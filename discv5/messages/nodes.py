from enr import ENR
from messages.message import Message


class NodesMessage(Message):
    nodes: list
    sender: ENR

    def __init__(self, nodes: list, sender: ENR) -> None:
        self.nodes = nodes
        self.sender = sender

    def get(self) -> list:
        return self.nodes

    def sender(self) -> ENR:
        return self.sender
