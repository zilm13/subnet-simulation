# Rewrite of UDP echo client/server example to use custom UDPEchoClient with Python

import ns.applications
import ns.core
import ns.internet
import ns.network
import ns.point_to_point
import pdb

ns.core.LogComponentEnable("UdpEchoClientCustomApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

nodes = ns.network.NodeContainer()
nodes.Create(2)

pointToPoint = ns.point_to_point.PointToPointHelper()
pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue("2ms"))

devices = pointToPoint.Install(nodes)

stack = ns.internet.InternetStackHelper()
stack.Install(nodes)

address = ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("10.1.1.0"),
                ns.network.Ipv4Mask("255.255.255.0"))

interfaces = address.Assign(devices)

echoServer = ns.applications.UdpEchoServerHelper(9)

serverApps = echoServer.Install(nodes.Get(1))
serverApps.Start(ns.core.Seconds(1.0))
serverApps.Stop(ns.core.Seconds(10.0))

echoClient = ns.applications.UdpEchoClientCustom()
nodes.Get(0).AddApplication(echoClient)
echoClient.SetRemote(interfaces.GetAddress(1), 9)
class Callback1(ns.applications.PythonCallback):
    a: int
    def __init__(self, a):
        self.a = a

    def isOverridden(self) -> bool:
        print ("isOverridden called")
        return True
    def getData(self) -> int:
        self.a += 1
        print ("a changed: " + str(self.a))
        return self.a
# pdb.set_trace()
d = Callback1(3)
echoClient.SetPythonCallback(d)
echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(5))
echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

clientApps = ns.network.ApplicationContainer(echoClient)
clientApps.Start(ns.core.Seconds(2.0))
clientApps.Stop(ns.core.Seconds(10.0))

ns.core.Simulator.Run()
ns.core.Simulator.Destroy()

