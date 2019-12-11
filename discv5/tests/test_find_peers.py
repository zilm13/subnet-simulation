from enr import ENR
from kademlia_table import KademliaTable
from messages.nodes import NodesMessage
from tasks.find_peers import FindPeersTask
from util import log_distance_sim


def test_find_peers():
    enr1 = ENR.from_values("127.0.0.1", 30303,
                           bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000"))
    enr2 = ENR.from_values("127.0.0.2", 30303,
                           bytes.fromhex("000000000000000000000000000000000000000000000000000000ff77555555"))
    enr3 = ENR.from_values("127.0.0.3", 30303,
                           bytes.fromhex("000000000000000000000000000000000000000000000000000000ffffffffff"))
    table = KademliaTable(enr1, [enr2, enr3])
    find_peers_from_1_to_2 = FindPeersTask(enr1, enr2, table)
    find_node_message1 = next(find_peers_from_1_to_2)
    assert find_node_message1.sender == enr1
    assert find_node_message1.distance == 1
    nodes = NodesMessage([enr3], enr2)
    assert log_distance_sim(enr2.id, enr3.id) == 4
    # make sure it's different to clarify absence of base bug
    assert log_distance_sim(enr1.id, enr3.id) == 5
    find_peers_from_1_to_2.parse(nodes.nodes)

    # latest peer was from 4th bucket but there was only 1 from it so it's not 100% that 4th bucket is over
    find_node_message2 = next(find_peers_from_1_to_2)
    assert find_node_message2.distance == 4

    # nothing changed until new parse
    find_node_message3 = next(find_peers_from_1_to_2)
    assert find_node_message3.distance == 4
