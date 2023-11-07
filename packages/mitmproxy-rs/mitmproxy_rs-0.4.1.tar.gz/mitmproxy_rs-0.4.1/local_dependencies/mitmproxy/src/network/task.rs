use std::cmp;
use std::collections::{HashMap, HashSet, VecDeque};
use std::fmt;
use std::net::SocketAddr;

use anyhow::Result;
use pretty_hex::pretty_hex;
use smoltcp::iface::{Config, SocketSet};
use smoltcp::socket::{tcp, Socket};

use smoltcp::wire::{
    HardwareAddress, Icmpv4Message, Icmpv4Packet, Icmpv4Repr, Icmpv6Message, Icmpv6Packet,
    Icmpv6Repr,
};
use smoltcp::{
    iface::{Interface, SocketHandle},
    phy::ChecksumCapabilities,
    time::{Duration, Instant},
    wire::{
        IpAddress, IpCidr, IpProtocol, IpRepr, Ipv4Address, Ipv4Packet, Ipv4Repr, Ipv6Address,
        Ipv6Packet, Ipv6Repr, TcpPacket, UdpPacket, UdpRepr,
    },
};
use tokio::sync::{
    broadcast,
    broadcast::Receiver as BroadcastReceiver,
    mpsc,
    mpsc::{Permit, Receiver, Sender, UnboundedReceiver},
    oneshot,
};
use tokio::task::JoinHandle;

use crate::messages::{
    ConnectionId, IpPacket, NetworkCommand, NetworkEvent, TransportCommand, TransportEvent,
    TunnelInfo,
};

use super::virtual_device::VirtualDevice;

/// Associated data for a smoltcp socket.
#[derive(Debug)]
pub(super) struct SocketData {
    handle: SocketHandle,
    /// smoltcp can only operate with fixed-size buffers, but Python's stream implementation assumes
    /// an infinite buffer. So we have a second send buffer here, plus a boolean to indicate that
    /// we want to send a FIN.
    send_buffer: VecDeque<u8>,
    write_eof: bool,
    // Gets notified once there's data to be read.
    recv_waiter: Option<(u32, oneshot::Sender<Vec<u8>>)>,
    // Gets notified once there is enough space in the write buffer.
    drain_waiter: Vec<oneshot::Sender<()>>,
    addr_tuple: (SocketAddr, SocketAddr),
}

struct NetworkIO<'a> {
    iface: Interface,
    device: VirtualDevice,
    sockets: SocketSet<'a>,

    net_tx: Sender<NetworkCommand>,

    socket_data: HashMap<ConnectionId, SocketData>,
    active_connections: HashSet<(SocketAddr, SocketAddr)>,
    next_connection_id: ConnectionId,
}

impl<'a> NetworkIO<'a> {
    fn new(net_tx: Sender<NetworkCommand>) -> Self {
        let mut device = VirtualDevice::new(net_tx.clone());

        let config = Config::new(HardwareAddress::Ip);
        let mut iface = Interface::new(config, &mut device, Instant::now());

        iface.set_any_ip(true);

        iface.update_ip_addrs(|ip_address| {
            ip_address
                .push(IpCidr::new(IpAddress::v4(0, 0, 0, 1), 0))
                .unwrap();
        });
        // TODO: IPv6
        iface
            .routes_mut()
            .add_default_ipv4_route(Ipv4Address::new(0, 0, 0, 1))
            .unwrap();

        NetworkIO {
            iface,
            device,
            sockets: SocketSet::new(Vec::new()),
            net_tx,
            socket_data: HashMap::new(),
            active_connections: HashSet::new(),
            next_connection_id: 0,
        }
    }

    fn receive_packet(
        &mut self,
        packet: IpPacket,
        tunnel_info: TunnelInfo,
        permit: Permit<'_, TransportEvent>,
    ) -> Result<()> {
        if let IpPacket::V4(p) = &packet {
            if !p.verify_checksum() {
                log::warn!("Received invalid IP packet (checksum error).");
                return Ok(());
            }
        }

        match packet.transport_protocol() {
            IpProtocol::Tcp => self.receive_packet_tcp(packet, tunnel_info, permit),
            IpProtocol::Udp => self.receive_packet_udp(packet, tunnel_info, permit),
            IpProtocol::Icmp => self.receive_packet_icmp(packet),
            _ => {
                log::debug!(
                    "Received IP packet for unknown protocol: {}",
                    packet.transport_protocol()
                );
                Ok(())
            }
        }
    }

    fn receive_packet_udp(
        &mut self,
        mut packet: IpPacket,
        tunnel_info: TunnelInfo,
        permit: Permit<'_, TransportEvent>,
    ) -> Result<()> {
        let src_ip = packet.src_ip();
        let dst_ip = packet.dst_ip();

        let mut udp_packet = match UdpPacket::new_checked(packet.payload_mut()) {
            Ok(p) => p,
            Err(e) => {
                log::debug!("Received invalid UDP packet: {}", e);
                return Ok(());
            }
        };

        let src_addr = SocketAddr::new(src_ip, udp_packet.src_port());
        let dst_addr = SocketAddr::new(dst_ip, udp_packet.dst_port());

        let event = TransportEvent::DatagramReceived {
            data: udp_packet.payload_mut().to_vec(),
            src_addr,
            dst_addr,
            tunnel_info,
        };

        permit.send(event);
        Ok(())
    }

    fn receive_packet_tcp(
        &mut self,
        mut packet: IpPacket,
        tunnel_info: TunnelInfo,
        permit: Permit<'_, TransportEvent>,
    ) -> Result<()> {
        let src_ip = packet.src_ip();
        let dst_ip = packet.dst_ip();

        let tcp_packet = match TcpPacket::new_checked(packet.payload_mut()) {
            // packet with correct length
            Ok(p) => {
                // packet with correct checksum
                if p.verify_checksum(&src_ip.into(), &dst_ip.into()) {
                    p
                } else {
                    // packet with incorrect checksum
                    log::warn!("Received invalid TCP packet (checksum error).");
                    return Ok(());
                }
            }
            // packet with incorrect length
            Err(e) => {
                log::debug!("Received invalid TCP packet ({}) with payload:", e);
                log::debug!("{}", pretty_hex(&packet.payload_mut()));
                return Ok(());
            }
        };

        let src_addr = SocketAddr::new(src_ip, tcp_packet.src_port());
        let dst_addr = SocketAddr::new(dst_ip, tcp_packet.dst_port());

        if tcp_packet.syn()
            && !tcp_packet.ack()
            && !self.active_connections.contains(&(src_addr, dst_addr))
        {
            let mut socket = tcp::Socket::new(
                tcp::SocketBuffer::new(vec![0u8; 64 * 1024]),
                tcp::SocketBuffer::new(vec![0u8; 64 * 1024]),
            );

            socket.listen(dst_addr)?;
            socket.set_timeout(Some(Duration::from_secs(60)));
            socket.set_keep_alive(Some(Duration::from_secs(28)));

            let handle = self.sockets.add(socket);

            let connection_id = {
                self.next_connection_id += 1;
                self.next_connection_id
            };

            let data = SocketData {
                handle,
                send_buffer: VecDeque::new(),
                write_eof: false,
                recv_waiter: None,
                drain_waiter: Vec::new(),
                addr_tuple: (src_addr, dst_addr),
            };
            self.socket_data.insert(connection_id, data);
            self.active_connections.insert((src_addr, dst_addr));

            let event = TransportEvent::ConnectionEstablished {
                connection_id,
                src_addr,
                dst_addr,
                tunnel_info,
            };
            permit.send(event);
        }

        self.device.receive_packet(packet);
        Ok(())
    }

    fn receive_packet_icmp(&mut self, packet: IpPacket) -> Result<()> {
        // Some apps check network connectivity by sending ICMP pings. ICMP traffic is currently
        // swallowed by mitmproxy_rs, which makes them believe that there is no network connectivity.
        // Generating fake ICMP replies as a simple workaround.

        if let Ok(permit) = self.net_tx.try_reserve() {
            // Generating and sending fake replies for ICMP echo requests. Ignoring all other ICMP types.
            let response_packet = match packet {
                IpPacket::V4(packet) => handle_icmpv4_echo_request(packet),
                IpPacket::V6(packet) => handle_icmpv6_echo_request(packet),
            };
            if let Some(response_packet) = response_packet {
                permit.send(NetworkCommand::SendPacket(response_packet));
            }
        } else {
            log::debug!("Channel full, discarding ICMP packet.");
        }
        Ok(())
    }

    fn read_data(&mut self, id: ConnectionId, n: u32, tx: oneshot::Sender<Vec<u8>>) {
        if let Some(data) = self.socket_data.get_mut(&id) {
            assert!(data.recv_waiter.is_none());
            data.recv_waiter = Some((n, tx));
        } else {
            // connection is has already been removed because the connection is closed,
            // so we just drop the tx.
        }
    }

    fn write_data(&mut self, id: ConnectionId, buf: Vec<u8>) {
        if let Some(data) = self.socket_data.get_mut(&id) {
            data.send_buffer.extend(buf);
        } else {
            // connection is has already been removed because the connection is closed,
            // so we just ignore the write.
        }
    }

    fn drain_writer(&mut self, id: ConnectionId, tx: oneshot::Sender<()>) {
        if let Some(data) = self.socket_data.get_mut(&id) {
            data.drain_waiter.push(tx);
        } else {
            // connection is has already been removed because the connection is closed,
            // so we just drop the tx.
        }
    }

    fn close_connection(&mut self, id: ConnectionId, _half_close: bool) {
        if let Some(data) = self.socket_data.get_mut(&id) {
            // smoltcp does not have a good way to do "SHUT_RDWR". We can't call .abort()
            // here because that sends a RST instead of a FIN (and breaks
            // retransmissions of the connection close packet). Alternatively, we could manually
            // set a timer on .close() and then forcibly .abort() once the timer expires (see
            // tcp-abort branch). This incurs a bit of unnecessary complexity, so we try something
            // dumber here: We simply close our end and then hope that either the client sends a FIN
            // or times out via the keepalive mechanism.

            data.write_eof = true;
        } else {
            // connection is already dead.
        }
    }

    fn send_datagram(&mut self, data: Vec<u8>, src_addr: SocketAddr, dst_addr: SocketAddr) {
        let permit = match self.net_tx.try_reserve() {
            Ok(p) => p,
            Err(_) => {
                log::debug!("Channel full, discarding UDP packet.");
                return;
            }
        };

        // We now know that there's space for us to send,
        // let's painstakingly reassemble the IP packet...

        let udp_repr = UdpRepr {
            src_port: src_addr.port(),
            dst_port: dst_addr.port(),
        };

        let ip_repr: IpRepr = match (src_addr, dst_addr) {
            (SocketAddr::V4(src_addr), SocketAddr::V4(dst_addr)) => IpRepr::Ipv4(Ipv4Repr {
                src_addr: Ipv4Address::from(*src_addr.ip()),
                dst_addr: Ipv4Address::from(*dst_addr.ip()),
                next_header: IpProtocol::Udp,
                payload_len: udp_repr.header_len() + data.len(),
                hop_limit: 255,
            }),
            (SocketAddr::V6(src_addr), SocketAddr::V6(dst_addr)) => IpRepr::Ipv6(Ipv6Repr {
                src_addr: Ipv6Address::from(*src_addr.ip()),
                dst_addr: Ipv6Address::from(*dst_addr.ip()),
                next_header: IpProtocol::Udp,
                payload_len: udp_repr.header_len() + data.len(),
                hop_limit: 255,
            }),
            _ => {
                log::error!("Failed to assemble UDP datagram: mismatched IP address versions");
                return;
            }
        };

        let buf = vec![0u8; ip_repr.buffer_len()];

        let mut ip_packet = match ip_repr {
            IpRepr::Ipv4(repr) => {
                let mut packet = Ipv4Packet::new_unchecked(buf);
                repr.emit(&mut packet, &ChecksumCapabilities::default());
                IpPacket::from(packet)
            }
            IpRepr::Ipv6(repr) => {
                let mut packet = Ipv6Packet::new_unchecked(buf);
                repr.emit(&mut packet);
                IpPacket::from(packet)
            }
        };

        udp_repr.emit(
            &mut UdpPacket::new_unchecked(ip_packet.payload_mut()),
            &ip_repr.src_addr(),
            &ip_repr.dst_addr(),
            data.len(),
            |buf| buf.copy_from_slice(data.as_slice()),
            &ChecksumCapabilities::default(),
        );

        permit.send(NetworkCommand::SendPacket(ip_packet));
    }

    fn handle_network_event(
        &mut self,
        event: NetworkEvent,
        permit: Permit<'_, TransportEvent>,
    ) -> Result<()> {
        match event {
            NetworkEvent::ReceivePacket {
                packet,
                tunnel_info,
            } => {
                self.receive_packet(packet, tunnel_info, permit)?;
            }
        }
        Ok(())
    }

    fn handle_transport_command(&mut self, command: TransportCommand) {
        match command {
            TransportCommand::ReadData(id, n, tx) => {
                self.read_data(id, n, tx);
            }
            TransportCommand::WriteData(id, buf) => {
                self.write_data(id, buf);
            }
            TransportCommand::DrainWriter(id, tx) => {
                self.drain_writer(id, tx);
            }
            TransportCommand::CloseConnection(id, half_close) => {
                self.close_connection(id, half_close);
            }
            TransportCommand::SendDatagram {
                data,
                src_addr,
                dst_addr,
            } => {
                self.send_datagram(data, src_addr, dst_addr);
            }
        }
    }
}

fn handle_icmpv4_echo_request(mut input_packet: Ipv4Packet<Vec<u8>>) -> Option<IpPacket> {
    let src_addr = input_packet.src_addr();
    let dst_addr = input_packet.dst_addr();

    // Parsing ICMP Packet
    let mut input_icmpv4_packet = match Icmpv4Packet::new_checked(input_packet.payload_mut()) {
        Ok(p) => p,
        Err(e) => {
            log::debug!("Received invalid ICMPv4 packet: {}", e);
            return None;
        }
    };

    // Checking that it is an ICMP Echo Request.
    if input_icmpv4_packet.msg_type() != Icmpv4Message::EchoRequest {
        log::debug!(
            "Unsupported ICMPv4 packet of type: {}",
            input_icmpv4_packet.msg_type()
        );
        return None;
    }

    // Creating fake response packet.
    let icmp_repr = Icmpv4Repr::EchoReply {
        ident: input_icmpv4_packet.echo_ident(),
        seq_no: input_icmpv4_packet.echo_seq_no(),
        data: input_icmpv4_packet.data_mut(),
    };
    let ip_repr = Ipv4Repr {
        // Directing fake reply back to the original source address.
        src_addr: dst_addr,
        dst_addr: src_addr,
        next_header: IpProtocol::Icmp,
        payload_len: icmp_repr.buffer_len(),
        hop_limit: 255,
    };
    let buf = vec![0u8; ip_repr.buffer_len() + icmp_repr.buffer_len()];
    let mut output_ipv4_packet = Ipv4Packet::new_unchecked(buf);
    ip_repr.emit(&mut output_ipv4_packet, &ChecksumCapabilities::default());
    let mut output_ip_packet = IpPacket::from(output_ipv4_packet);
    icmp_repr.emit(
        &mut Icmpv4Packet::new_unchecked(output_ip_packet.payload_mut()),
        &ChecksumCapabilities::default(),
    );
    Some(output_ip_packet)
}

fn handle_icmpv6_echo_request(mut input_packet: Ipv6Packet<Vec<u8>>) -> Option<IpPacket> {
    let src_addr = input_packet.src_addr();
    let dst_addr = input_packet.dst_addr();

    // Parsing ICMP Packet
    let mut input_icmpv6_packet = match Icmpv6Packet::new_checked(input_packet.payload_mut()) {
        Ok(p) => p,
        Err(e) => {
            log::debug!("Received invalid ICMPv6 packet: {}", e);
            return None;
        }
    };

    // Checking that it is an ICMP Echo Request.
    if input_icmpv6_packet.msg_type() != Icmpv6Message::EchoRequest {
        log::debug!(
            "Unsupported ICMPv6 packet of type: {}",
            input_icmpv6_packet.msg_type()
        );
        return None;
    }

    // Creating fake response packet.
    let icmp_repr = Icmpv6Repr::EchoReply {
        ident: input_icmpv6_packet.echo_ident(),
        seq_no: input_icmpv6_packet.echo_seq_no(),
        data: input_icmpv6_packet.payload_mut(),
    };
    let ip_repr = Ipv6Repr {
        // Directing fake reply back to the original source address.
        src_addr: dst_addr,
        dst_addr: src_addr,
        next_header: IpProtocol::Icmp,
        payload_len: icmp_repr.buffer_len(),
        hop_limit: 255,
    };
    let buf = vec![0u8; ip_repr.buffer_len() + icmp_repr.buffer_len()];
    let mut output_ipv6_packet = Ipv6Packet::new_unchecked(buf);
    ip_repr.emit(&mut output_ipv6_packet);
    let mut output_ip_packet = IpPacket::from(output_ipv6_packet);
    icmp_repr.emit(
        // Directing fake reply back to the original source address.
        &IpAddress::from(dst_addr),
        &IpAddress::from(src_addr),
        &mut Icmpv6Packet::new_unchecked(output_ip_packet.payload_mut()),
        &ChecksumCapabilities::default(),
    );
    Some(output_ip_packet)
}

pub struct NetworkTask<'a> {
    net_tx: Sender<NetworkCommand>,
    net_rx: Receiver<NetworkEvent>,
    py_tx: Sender<TransportEvent>,
    py_rx: UnboundedReceiver<TransportCommand>,

    shutdown: BroadcastReceiver<()>,
    io: NetworkIO<'a>,
}

#[allow(clippy::type_complexity)]
pub fn add_network_layer(
    transport_events_tx: Sender<TransportEvent>,
    transport_commands_rx: UnboundedReceiver<TransportCommand>,
    shutdown: broadcast::Receiver<()>,
) -> Result<(
    JoinHandle<Result<()>>,
    Sender<NetworkEvent>,
    Receiver<NetworkCommand>,
)> {
    // initialize channels between the WireGuard server and the virtual network device
    let (network_events_tx, network_events_rx) = mpsc::channel(256);
    let (network_commands_tx, network_commands_rx) = mpsc::channel(256);

    let task = NetworkTask::new(
        network_commands_tx,
        network_events_rx,
        transport_events_tx,
        transport_commands_rx,
        shutdown,
    )?;
    let h = tokio::spawn(async move { task.run().await });
    Ok((h, network_events_tx, network_commands_rx))
}

impl NetworkTask<'_> {
    pub fn new(
        net_tx: Sender<NetworkCommand>,
        net_rx: Receiver<NetworkEvent>,
        py_tx: Sender<TransportEvent>,
        py_rx: UnboundedReceiver<TransportCommand>,
        sd_watcher: BroadcastReceiver<()>,
    ) -> Result<Self> {
        let io = NetworkIO::new(net_tx.clone());
        Ok(Self {
            net_tx,
            net_rx,
            py_tx,
            py_rx,
            shutdown: sd_watcher,
            io,
        })
    }

    pub async fn run(mut self) -> Result<()> {
        let mut io = self.io;
        let mut remove_conns = Vec::new();

        let mut py_tx_permit: Option<Permit<TransportEvent>> = None;

        'task: loop {
            // On a high level, we do three things in our main loop:
            // 1. Wait for an event from either side and handle it, or wait until the next smoltcp timeout.
            // 2. `.poll()` the smoltcp interface until it's finished with everything for now.
            // 3. Check if we can wake up any waiters, move more data in the send buffer, or clean up sockets.

            // check device for timeouts
            let delay = io.iface.poll_delay(Instant::now(), &io.sockets);

            #[cfg(debug_assertions)]
            if let Some(d) = delay {
                log::debug!("Waiting for device timeout: {} ...", d);
            }

            #[cfg(debug_assertions)]
            log::debug!("Waiting for events ...");

            if py_tx_permit.is_none() {
                py_tx_permit = self.py_tx.try_reserve().ok();
            }
            let net_tx_full = self.net_tx.capacity() == 0;

            tokio::select! {
                // wait for graceful shutdown
                _ = self.shutdown.recv() => break 'task,
                // wait for timeouts when the device is idle
                _ = async { tokio::time::sleep(delay.unwrap().into()).await }, if delay.is_some() => {},
                // wait for incoming packets
                Some(e) = self.net_rx.recv(), if py_tx_permit.is_some() => {
                    // handle pending network events until channel is full
                    io.handle_network_event(e, py_tx_permit.take().unwrap())?;

                    while let Ok(p) = self.py_tx.try_reserve() {
                        if let Ok(e) = self.net_rx.try_recv() {
                            io.handle_network_event(e, p)?;
                        } else {
                            break;
                        }
                    }
                },
                // wait for outgoing packets
                Some(c) = self.py_rx.recv(), if !net_tx_full => {
                    // handle pending transport commands until channel is full
                    io.handle_transport_command(c);

                    while self.net_tx.capacity() > 0 {
                        if let Ok(c) = self.py_rx.try_recv() {
                            io.handle_transport_command(c);
                        } else {
                            break;
                        }
                    }
                },
                // wait until channels are no longer full
                Ok(()) = wait_for_channel_capacity(&self.py_tx), if py_tx_permit.is_none() => {},
                Ok(()) = wait_for_channel_capacity(&self.net_tx), if net_tx_full => {},
            }

            // poll virtual network device
            #[cfg(debug_assertions)]
            log::debug!("Polling virtual network device ...");
            io.iface
                .poll(Instant::now(), &mut io.device, &mut io.sockets);

            #[cfg(debug_assertions)]
            log::debug!("Processing TCP connections ...");

            for (connection_id, data) in io.socket_data.iter_mut() {
                let socket = io.sockets.get_mut::<tcp::Socket>(data.handle);

                // receive data over the socket
                if data.recv_waiter.is_some() {
                    if socket.can_recv() {
                        let (n, tx) = data.recv_waiter.take().unwrap();
                        let bytes_available = socket.recv_queue();

                        let mut buf = vec![0u8; cmp::min(bytes_available, n as usize)];
                        let bytes_read = socket.recv_slice(&mut buf)?;

                        buf.truncate(bytes_read);
                        if tx.send(buf).is_err() {
                            log::debug!("Cannot send received data, channel was already closed.");
                        }
                    } else {
                        // We can't use .may_recv() here as it returns false during establishment.
                        use tcp::State::*;
                        match socket.state() {
                            // can we still receive something in the future?
                            CloseWait | LastAck | Closed | Closing | TimeWait => {
                                let (_, tx) = data.recv_waiter.take().unwrap();
                                if tx.send(Vec::new()).is_err() {
                                    log::debug!("Cannot send close, channel was already closed.");
                                }
                            }
                            _ => {}
                        }
                    }
                }

                // send data over the socket
                if !data.send_buffer.is_empty() && socket.can_send() {
                    let (a, b) = data.send_buffer.as_slices();
                    let sent = socket.send_slice(a)? + socket.send_slice(b)?;
                    data.send_buffer.drain(..sent);
                }

                // if necessary, drain write buffers:
                // either when drain has been requested explicitly, or when socket is being closed
                // TODO: benchmark different variants here. (e.g. only return on half capacity)
                if (!data.drain_waiter.is_empty() || data.write_eof)
                    && socket.send_queue() < socket.send_capacity()
                {
                    for waiter in data.drain_waiter.drain(..) {
                        if waiter.send(()).is_err() {
                            log::debug!("TcpStream already closed, cannot send notification about drained buffers.")
                        }
                    }
                }

                #[cfg(debug_assertions)]
                log::debug!(
                    "TCP connection {}: socket state {} for {:?}",
                    connection_id,
                    socket.state(),
                    data.addr_tuple,
                );

                // if requested, close socket
                if data.write_eof && data.send_buffer.is_empty() {
                    socket.close();
                    data.write_eof = false;
                }

                // if socket is closed, mark connection for removal
                if socket.state() == tcp::State::Closed {
                    remove_conns.push(*connection_id);
                }
            }

            for connection_id in remove_conns.drain(..) {
                let data = io.socket_data.remove(&connection_id).unwrap();
                io.sockets.remove(data.handle);
                io.active_connections.remove(&data.addr_tuple);
            }

            // poll again. we may have new stuff to do.
            #[cfg(debug_assertions)]
            log::debug!("Polling virtual network device ...");
            io.iface
                .poll(Instant::now(), &mut io.device, &mut io.sockets);
        }

        // TODO: process remaining pending data after the shutdown request was received?

        log::debug!("Virtual Network device task shutting down.");
        Ok(())
    }
}

impl fmt::Debug for NetworkTask<'_> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let sockets: Vec<String> = self
            .io
            .sockets
            .iter()
            .filter_map(|(_h, s)| match s {
                Socket::Tcp(s) => Some(s),
                _ => None,
            })
            .map(|sock| {
                format!(
                    "TCP {:<21} {:<21} {}",
                    sock.remote_endpoint()
                        .map(|e| e.to_string())
                        .as_ref()
                        .map_or("not connected", String::as_str),
                    sock.local_endpoint()
                        .map(|e| e.to_string())
                        .as_ref()
                        .map_or("not connected", String::as_str),
                    sock.state()
                )
            })
            .collect();

        f.debug_struct("NetworkTask")
            .field("sockets", &sockets)
            .finish()
    }
}

async fn wait_for_channel_capacity<T>(s: &Sender<T>) -> Result<()> {
    let permit = s.reserve().await?;
    drop(permit);
    Ok(())
}
