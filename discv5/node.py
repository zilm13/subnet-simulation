from collections import deque
from typing import (NamedTuple, Callable)

from config import BUCKETS
from enr import ENR
from kademlia_table import (KademliaTable)
from messages.findnode import FindNodeMessage
from messages.message import Message
from messages.nodes import NodesMessage
from tasks.find_peers import FindPeersRoutine


class FindPeerTaskStatus(NamedTuple):
    nodes: deque
    current_bucket: int

    @classmethod
    def from_values(cls, nodes: list, current_bucket: int):
        return cls(deque(nodes), current_bucket)

    def is_empty(self) -> bool:
        return len(self.nodes) == 0


class Node():
    home: ENR
    table: KademliaTable
    find_peers: FindPeersRoutine
    status: FindPeerTaskStatus
    send_callback: Callable[[Message, ENR], None]

    def __init__(self, home: ENR, boot_nodes: list, send_callback: Callable[[Message, ENR], None]) -> None:
        self.home = home
        self.send_callback = send_callback
        self.table = KademliaTable(home, boot_nodes)
        self.find_peers = FindPeersRoutine(home, self.table)
        self.status = FindPeerTaskStatus(list(), 0)

    # forces one step of node life
    def tick(self):
        if self.status.is_empty():
            new_bucket = self.status.current_bucket + 1
            if new_bucket > BUCKETS:
                new_bucket = 1
            nodes = self.table.find_strict(new_bucket)
            # TODO: handle empty nodes
            self.status = FindPeerTaskStatus(nodes, new_bucket)

        if not self.status.is_empty():
            self.find_peers.generate(self.status.nodes.pop())

    def send(self, message: Message, to: ENR) -> None:
        self.send_callback(message, to)

    def handle(self, message: Message) -> None:
        if type(message) == FindNodeMessage:
            reply = NodesMessage(self.table.find(message.distance), self.home)
            self.send(reply, message.sender)
        else:
            raise Exception("Not supported message")

    def table(self) -> KademliaTable:
        return self.table
