import os

from enr import ENR
from messages.message import Message
from node import Node
from util import log_distance_sim


class Router():
    routing: dict

    def __init__(self) -> None:
        super().__init__()
        self.routing = dict()

    def register(self, enr: ENR, node: Node):
        self.routing[enr] = node

    def send(self, message: Message, recipient: ENR):
        if recipient in self.routing:
            self.routing[recipient].handle(message)
        else:
            raise Exception("Recipient " + str(recipient) + " not found!")


def test_p2p():
    router = Router()
    enr1 = ENR.from_values("127.0.0.1", 30303, os.urandom(32))
    enr2 = ENR.from_values("127.0.0.2", 30303, os.urandom(32))
    enr3 = ENR.from_values("127.0.0.3", 30303, os.urandom(32))
    n1 = Node(enr1, [enr2, enr3], router.send)
    router.register(enr1, n1)
    n2 = Node(enr2, [enr1], router.send)
    router.register(enr2, n2)
    n3 = Node(enr3, [], router.send)
    router.register(enr3, n3)
    for i in range(0, 32):
        n1.tick()
        n2.tick()
    id2_id3_distance = log_distance_sim(enr2.id, enr3.id)
    print("\nid2_id3_distance: " + str(id2_id3_distance) + "\n")
    assert enr3 in n2.table.find_strict(id2_id3_distance)
