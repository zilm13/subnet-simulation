from config import K
from enr import ENR
from kademlia_table import KademliaTable, Bucket
from util import log_distance_sim


def test_bucket():
    # just to be clear that logic of this test depends on K's exact value
    assert K == 4
    enr1 = ENR.from_values("127.0.0.1", 30303,
                           bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000001"))
    enr2 = ENR.from_values("127.0.0.2", 30303,
                           bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000002"))
    enr3 = ENR.from_values("127.0.0.3", 30303,
                           bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000003"))
    enr4 = ENR.from_values("127.0.0.3", 30303,
                           bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000004"))
    enr5 = ENR.from_values("127.0.0.3", 30303,
                           bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000005"))
    enr6 = ENR.from_values("127.0.0.3", 30303,
                           bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000006"))
    bucket = Bucket()
    bucket.put(enr1)
    assert len(bucket) == 1
    bucket.put(enr2)
    bucket.put(enr3)
    bucket.put(enr4)
    # bucket == enr1 enr2 enr3 enr4
    assert len(bucket) == 4
    bucket.put(enr1)
    # bucket == enr2 enr3 enr4 enr1
    assert len(bucket) == 4
    bucket.put(enr5)
    bucket.put(enr6)
    # bucket == enr4 enr1 enr5 enr6
    assert len(bucket) == 4
    assert enr4 in bucket
    assert enr1 in bucket
    assert enr5 in bucket
    assert enr6 in bucket


def test_kademlia_table():
    enr1 = ENR.from_values("127.0.0.1", 30303,
                           bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000"))
    enr2 = ENR.from_values("127.0.0.2", 30303,
                           bytes.fromhex("000000000000000000000000000000000000000000000000000000000000000f"))
    enr3 = ENR.from_values("127.0.0.3", 30303,
                           bytes.fromhex("00000000000000000000000000000000000000000000000000000000ffffffff"))
    table = KademliaTable(enr1, [enr2, enr3])
    nodes_find = table.find(1)
    assert len(nodes_find) == 2
    assert enr2 in nodes_find
    assert enr3 in nodes_find
    assert log_distance_sim(enr1.id, enr2.id) == 1
    assert log_distance_sim(enr1.id, enr3.id) == 4
    nodes_find_strict1 = table.find_strict(1)
    assert len(nodes_find_strict1) == 1
    assert enr2 in nodes_find_strict1
    nodes_find_strict2 = table.find_strict(2)
    assert len(nodes_find_strict2) == 0
    nodes_find_strict4 = table.find_strict(4)
    assert len(nodes_find_strict4) == 1
    assert enr3 in nodes_find_strict4
    nodes_find_from5 = table.find(5)
    assert len(nodes_find_from5) == 0
