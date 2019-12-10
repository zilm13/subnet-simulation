from enr import ENR
from kademlia_table import KademliaTable
from messages.nodes import NodesMessage
from tasks.find_peers import FindPeersRoutine
from util import log_distance_sim


def test_find_peers():
    enr1 = ENR.from_values("127.0.0.1", 30303,
                           bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000"))
    enr2 = ENR.from_values("127.0.0.2", 30303,
                           bytes.fromhex("000000000000000000000000000000000000000000000000000000000000000f"))
    enr3 = ENR.from_values("127.0.0.3", 30303,
                           bytes.fromhex("00000000000000000000000000000000000000000000000000000000ffffffff"))
    table = KademliaTable(enr1, [enr2, enr3])
    find_peers = FindPeersRoutine(enr1, table)
    find_node_message1 = find_peers.generate(enr2)
    assert find_node_message1.sender == enr1
    assert find_node_message1.distance == 1
    nodes = NodesMessage([enr3], enr2)
    assert log_distance_sim(enr2.id, enr3.id) == 4
    find_peers.parse(nodes)

    # latest peer was from 4th bucket but there was only 1 from it so it's not 100% that 4th bucket is over
    find_node_message2 = find_peers.generate(enr2)
    assert find_node_message2.distance == 4

    # nothing changed until parse
    find_node_message3 = find_peers.generate(enr2)
    assert find_node_message3.distance == 4

    # nothing changed for any other enr2
    find_node_message4 = find_peers.generate(enr3)
    assert find_node_message4.distance == 1
