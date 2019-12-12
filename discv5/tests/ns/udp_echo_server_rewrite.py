from typing import Callable

import ns.network
import ns.core


class UdpEchoServer(ns.network.Application):
    """
    Rewrite of ns.applications.UdpEchoServer
    """
    m_port: int
    m_local: ns.network.Address
    m_socket: ns.network.Socket
    m_socket6: ns.network.Socket
    m_rxTrace: Callable[[ns.network.Packet], None]
    m_rxTraceWithAddresses: Callable[[ns.network.Packet, ns.network.Address, ns.network.Address], None]

    def __init__(self) -> None:
        super().__init__()
        ns.core.NS_LOG_COMPONENT_DEFINE("UdpEchoServerApplication")
        ns.core.NS_OBJECT_ENSURE_REGISTERED(UdpEchoServer)
        ns.core.NS_LOG_FUNCTION(self)
        self.m_socket = 0
        self.m_socket6 = 0

    def GetTypeId(self):
        tid = ns.core.TypeId("ns3::UdpEchoServer") \
            .SetParent(ns.network.Application) \
            .SetGroupName("Applications") \
            .AddConstructor(UdpEchoServer) \
            .AddAttribute("Port", "Port on which we listen for incoming packets.",
                          ns.core.UintegerValue(9),
                          ns.core.MakeUintegerAccessor(self.m_port),
                          # FIXME <uint16_t> param below
                          ns.core.MakeUintegerChecker()) \
            .AddTraceSource("Rx", "A packet has been received",
                            ns.core.MakeTraceSourceAccessor(self.m_rxTrace),
                            "ns3::Packet::TracedCallback") \
            .AddTraceSource("RxWithAddresses", "A packet has been received",
                            ns.core.MakeTraceSourceAccessor(self.m_rxTraceWithAddresses),
                            "ns3::Packet::TwoAddressTracedCallback")
        return tid

    def StartApplication(self):
        ns.core.NS_LOG_FUNCTION(self)
        if self.m_socket == 0:
            tid = ns.core.TypeId.LookupByName("ns3::UdpSocketFactory")
            self.m_socket = ns.network.Socket.CreateSocket(super().GetNode(), tid)
            local = ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), self.m_port)
            if self.m_socket.Bind(local) == -1:
                ns.core.NS_FATAL_ERROR("Failed to bind socket")
            if ns.network.addressUtils.IsMulticast(self.m_local):
                udpSocket = ns.network.UdpSocket(self.m_socket)
                if udpSocket is not None:
                    udpSocket.MulticastJoinGroup(0, self.m_local)
                else:
                    ns.core.NS_FATAL_ERROR("Error: Failed to join multicast group")

        if self.m_socket6 == 0:
            tid = ns.core.TypeId.LookupByName("ns3::UdpSocketFactory")
            self.m_socket6 = ns.network.Socket.CreateSocket(super().GetNode(), tid)
            local6 = ns.network.Inet6SocketAddress(ns.network.Ipv6Address.GetAny(), self.m_port)
            if self.m_socket6.Bind(local6) == -1:
                ns.core.NS_FATAL_ERROR("Failed to bind socket")
            if ns.network.addressUtils.IsMulticast(local6):
                udpSocket = ns.network.UdpSocket(self.m_socket6)
                if udpSocket is not None:
                    udpSocket.MulticastJoinGroup(0, local6)
                else:
                    ns.core.NS_FATAL_ERROR("Error: Failed to join multicast group")

        self.m_socket.SetRecvCallback(ns.core.MakeCallback(self.HandleRead, self))
        self.m_socket6.SetRecvCallback(ns.core.MakeCallback(self.HandleRead, self))

    def StopApplication(self):
        self.NS_LOG_FUNCTION(self)
        if self.m_socket != 0:
            self.m_socket.Close()
            self.m_socket.SetRecvCallback(ns.core.MakeNullCallback())
        if self.m_socket6 != 0:
            self.m_socket6.Close()
            self.m_socket6.SetRecvCallback(ns.core.MakeNullCallback())

    def HandleRead(self, socket: ns.network.Socket):
        self.NS_LOG_FUNCTION(self, socket)
        for packet in socket:
            from_addr = None
            socket.RecvFrom(from_addr)
            localAddress = None
            socket.GetSockName(localAddress)
            self.m_rxTrace(packet)
            self.m_rxTraceWithAddresses(packet, from_addr, localAddress)
            if ns.network.InetSocketAddress.IsMatchingType(from_addr):
                ns.core.NS_LOG_INFO("At time " + str(ns.core.Simulator.Now().GetSeconds()) + "s server received " + str(
                    packet.GetSize()) + " bytes from " + str(
                    ns.network.InetSocketAddress.ConvertFrom(from_addr).GetIpv4()) + " port " + str(
                    ns.network.InetSocketAddress.ConvertFrom(from_addr).GetPort()))
            elif ns.network.Inet6SocketAddress.IsMatchingType(from_addr):
                ns.core.NS_LOG_INFO("At time " + str(ns.core.Simulator.Now().GetSeconds()) + "s server received " + str(
                    packet.GetSize()) + " bytes from " + str(
                    ns.network.Inet6SocketAddress.ConvertFrom(from_addr).GetIpv6()) + " port " + str(
                    ns.network.Inet6SocketAddress.ConvertFrom(from_addr).GetPort()))

            packet.RemoveAllPacketTags()
            packet.RemoveAllByteTags()

            ns.core.NS_LOG_LOGIC("Echoing packet")
            socket.SendTo(packet, 0, from_addr)

            if ns.network.InetSocketAddress.IsMatchingType(from_addr):
                ns.core.NS_LOG_INFO("At time " + str(ns.core.Simulator.Now().GetSeconds()) + "s server sent " + str(
                    packet.GetSize()) + " bytes to " + str(
                    ns.network.InetSocketAddress.ConvertFrom(from_addr).GetIpv4()) + " port " + str(
                    ns.network.InetSocketAddress.ConvertFrom(from_addr).GetPort()))
            elif ns.network.Inet6SocketAddress.IsMatchingType(from_addr):
                ns.core.NS_LOG_INFO("At time " + str(ns.core.Simulator.Now().GetSeconds()) + "s server sent " + str(
                    packet.GetSize()) + " bytes to " + str(
                    ns.network.Inet6SocketAddress.ConvertFrom(from_addr).GetIpv6()) + " port " + str(
                    ns.network.Inet6SocketAddress.ConvertFrom(from_addr).GetPort()))
