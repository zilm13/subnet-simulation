# TODO: Start network layer with NS3 here
import ns.core
import ns.network
import ns.csma
import ns.internet
import ns.applications
import sys

cmd = ns.core.CommandLine()
cmd.nCsma = 3
cmd.verbose = "True"
cmd.AddValue("nCsma", "Number of \"extra\" CSMA nodes/devices")
cmd.AddValue("verbose", "Tell echo applications to log if true")
cmd.Parse(sys.argv)

nCsma = int(cmd.nCsma)
verbose = cmd.verbose

if verbose == "True":
	ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
	ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)
nCsma = 1 if int(nCsma) == 0 else int(nCsma)

csmaNodes = ns.network.NodeContainer()
csmaNodes.Create(nCsma)

csma = ns.csma.CsmaHelper()
csma.SetChannelAttribute("DataRate", ns.core.StringValue("100Mbps"))
csma.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.NanoSeconds(6560)))

csmaDevices = csma.Install(csmaNodes)

stack = ns.internet.InternetStackHelper()
stack.Install(csmaNodes)

address = ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("10.1.2.0"), ns.network.Ipv4Mask("255.255.255.0"))
csmaInterfaces = address.Assign(csmaDevices)

# TODO
#
# echoServer = ns.applications.UdpEchoServerHelper(9)
#
# serverApps = echoServer.Install(csmaNodes.Get(nCsma))
# serverApps.Start(ns.core.Seconds(1.0))
# serverApps.Stop(ns.core.Seconds(10.0))
#
# echoClient = ns.applications.UdpEchoClientHelper(csmaInterfaces.GetAddress(nCsma), 9)
# echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
# echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds (1.0)))
# echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))
#
# clientApps = echoClient.Install(p2pNodes.Get(0))
# clientApps.Start(ns.core.Seconds(2.0))
# clientApps.Stop(ns.core.Seconds(10.0))

ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()

csma.EnablePcap ("second", csmaDevices.Get (1), True)

ns.core.Simulator.Run()
ns.core.Simulator.Destroy()

