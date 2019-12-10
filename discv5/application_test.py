import os

from enr import ENR
from node import Node
from messages.message import Message
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
            raise Exception("Recipient " + recipient + " not found!")


def p2p_test():
    router = Router()
    enr1 = ENR("127.0.0.1", 30303, os.urandom(32))
    enr2 = ENR("127.0.0.2", 30303, os.urandom(32))
    enr3 = ENR("127.0.0.3", 30303, os.urandom(32))
    n1 = Node(enr1, [enr2, enr3], router.send)
    n2 = Node(enr2, [enr1], router.send)
    for i in range (0, 32):
        n1.tick()
        n2.tick()
    id2_id3_distance = log_distance_sim(enr2.id, enr3.id)
    assert enr3 in n2.table().find_strict(id2_id3_distance)
