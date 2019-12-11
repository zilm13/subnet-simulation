from typing import List

from enr import ENR
from messages.message import Message


class NodesMessage(Message):
    nodes: list

    def __init__(self, nodes: List[ENR], sender: ENR) -> None:
        super().__init__(sender)
        self.nodes = nodes

    def __str__(self) -> str:
        return "NodesMessage[" + super().__str__() + ", nodes: (" + str(len(self.nodes)) + " total)" + ", ".join(
            [str(node) for node in self.nodes])
