from typing import NamedTuple

from config import (K, BUCKETS, MAX_FIND_PEERS)
from enr import ENR
from kademlia_table import KademliaTable
from messages.findnode import FindNodeMessage
from messages.nodes import NodesMessage
from util import log_distance_sim


class FindTaskStatus(NamedTuple):
    next_distance: int
    total_discovered: int

    def __init__(self) -> None:
        super.__init__(self)
        self.next_distance = 1
        self.total_discovered = 0


class FindPeersTask():
    tasks: dict
    home: ENR
    table: KademliaTable

    def __init__(self, home: ENR, table: KademliaTable) -> None:
        self.tasks = dict()
        self.home = home
        self.table = table

    def generate(self, enr: ENR) -> FindNodeMessage:
        if enr not in self.tasks:
            # requests are started from bucket #1
            self.tasks[enr] = FindTaskStatus()
        return FindNodeMessage(self.tasks[enr].next_distance)

    def parse(self, nodes: NodesMessage):
        if len(nodes.get()) == 0:
            return
        current_bucket = log_distance_sim(self.home.id, nodes.get()[0].id)
        nodes_in_bucket = 0
        task = self.tasks[nodes.sender()]
        for node in nodes.get():
            node_bucket = log_distance_sim(self.home.id, node.id)
            if node_bucket != current_bucket:
                current_bucket = node_bucket
                nodes_in_bucket = 0
            nodes_in_bucket += 1
            task.total_discovered += 1
            self.table.put(node)
        next_bucket = current_bucket

        # Last bucket fully dispatched
        if nodes_in_bucket == K:
            next_bucket += 1

        # node tracing is over
        if next_bucket > BUCKETS or task.total_discovered >= MAX_FIND_PEERS:
            del task
        else:
            task.next_distance = next_bucket
