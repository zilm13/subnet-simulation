from typing import List

from enr import ENR
from messages.message import Message


class NodesMessage(Message):
    nodes: list

    def __init__(self, nodes: List[ENR], sender: ENR) -> None:
        super().__init__(sender)
        self.nodes = nodes

    def get(self) -> List[ENR]:
        return self.nodes
