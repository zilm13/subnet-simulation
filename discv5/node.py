from collections import deque
from typing import (NamedTuple, Callable)

from kademlia_table import (KademliaTable, Bucket)
from task.find_peers import FindPeersTask
from enr import ENR
from config import BUCKETS
from messages.message import Message
from messages.findnode import FindNodeMessage
from messages.nodes import NodesMessage


class FindPeerTaskStatus(NamedTuple):
    nodes: deque
    current_bucket: int

    def __init__(self, nodes: list, current_bucket: int) -> None:
        super.__init__(self)
        self.nodes = deque(nodes)
        self.current_bucket = current_bucket

    def is_empty(self) -> bool:
        return len(self.nodes) == 0


class Node():
    home: ENR
    table: KademliaTable
    find_peers: FindPeersTask
    status: FindPeerTaskStatus
    send_callback: Callable[[Message, ENR], None]

    def __init__(self, home: ENR, boot_nodes: list, send_callback: Callable[[Message, ENR], None]) -> None:
        self.home = home
        self.send_callback = send_callback
        self.table = KademliaTable(home, boot_nodes)
        self.find_peers = FindPeersTask(home, self.table)
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
            reply = NodesMessage(self.table.find(message.get()), self.home)
            self.send(reply, message.sender())
        else:
            raise Exception("Not supported message")

    def table(self) -> KademliaTable:
        return self.table


