from enr import ENR
from messages.message import Message


class NodesMessage(Message):
    nodes: list

    def __init__(self, nodes: list, sender: ENR) -> None:
        super().__init__(sender)
        self.nodes = nodes

    def get(self) -> list:
        return self.nodes
