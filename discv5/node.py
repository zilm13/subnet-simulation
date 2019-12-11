import logging
from collections import deque
from typing import (Deque, List, NamedTuple, Callable, Sequence)

from config import BUCKETS
from enr import ENR
from kademlia_table import (KademliaTable)
from messages.findnode import FindNodeMessage
from messages.message import Message
from messages.nodes import NodesMessage
from tasks.find_peers import FindPeersTask


class FindPeerTaskStatus(NamedTuple):
    nodes: Deque[ENR]
    current_bucket: int
    current_task: FindPeersTask

    @classmethod
    def from_values(cls, nodes: Sequence[ENR], current_bucket: int, home: ENR, table: KademliaTable):
        assert len(nodes) > 0
        assert isinstance(nodes, list) or isinstance(nodes, deque)
        task = FindPeersTask(home, nodes[0], table)
        if isinstance(nodes, list):
            return cls(deque(nodes[1:]), current_bucket, task)
        else:
            nodes.pop()
            return cls(deque(nodes), current_bucket, task)

    @classmethod
    def empty(cls):
        return cls(deque(), 0, None)

    def is_empty(self) -> bool:
        return len(self.nodes) == 0 and (self.current_task is None or not self.current_task.has_next())


class Node():
    home: ENR
    table: KademliaTable
    status: FindPeerTaskStatus
    send_callback: Callable[[Message, ENR], None]
    logger: logging.Logger

    def __init__(self, home: ENR, boot_nodes: List[ENR], send_callback: Callable[[Message, ENR], None]) -> None:
        self.home = home
        self.send_callback = send_callback
        self.table = KademliaTable(home, boot_nodes)
        self.status = FindPeerTaskStatus.empty()
        self.logger = logging.getLogger(__name__)

    # forces one step of node life
    def tick(self):
        self.logger.debug("Tick for " + str(self.home))
        steps = 0
        new_bucket = self.status.current_bucket + 1
        while self.status.is_empty() and steps < BUCKETS:
            # so we are not going to cycle with empty KademliaTable
            steps += 1
            if new_bucket > BUCKETS:
                new_bucket = 1
            # self.logger.debug("find_strict in " + str(self.home) + ", bucket: " + str(new_bucket))
            nodes = self.table.find_strict(new_bucket)
            if len(nodes) > 0:
                self.status = FindPeerTaskStatus.from_values(nodes, new_bucket, self.home, self.table)
            else:
                new_bucket += 1

        if not self.status.is_empty():
            self.logger.debug("We have tasks in " + str(self.home))
            # TODO: parallel tasks
            if not self.status.current_task.has_next():
                self.status = FindPeerTaskStatus.from_values(self.status.nodes, self.status.current_bucket, self.home,
                                                             self.table)
            message = next(self.status.current_task)
            self.send(message, self.status.current_task.recipient)

    def send(self, message: Message, to: ENR) -> None:
        self.logger.debug("Send in " + str(self.home) + ". Message: " + str(message) + ". To: " + str(to))
        self.send_callback(message, to)

    def handle(self, message: Message) -> None:
        self.logger.debug("Handle incoming in " + str(self.home) + ". Message: " + str(message))
        if type(message) == FindNodeMessage:
            reply = NodesMessage(self.table.find(message.distance), self.home)
            self.send(reply, message.sender)
        elif type(message) == NodesMessage:
            self.status.current_task.parse(message.nodes)
        else:
            raise Exception("Not supported message")
