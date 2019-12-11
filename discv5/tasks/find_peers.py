from typing import (Dict, NamedTuple)

from config import (K, BUCKETS, MAX_FIND_PEERS)
from enr import ENR
from kademlia_table import KademliaTable
from messages.findnode import FindNodeMessage
from messages.nodes import NodesMessage
from util import log_distance_sim


class FindPeersStatus(NamedTuple):
    next_distance: int
    total_discovered: int

    @classmethod
    def default(cls):
        return cls(1, 0)

    def from_values(cls, next_distance: int, total_discovered: int):
        return cls(next_distance, total_discovered)


class FindPeersRoutine():
    tasks: Dict[ENR, FindPeersStatus]
    home: ENR
    table: KademliaTable

    def __init__(self, home: ENR, table: KademliaTable) -> None:
        self.tasks = dict()
        self.home = home
        self.table = table

    def generate(self, enr: ENR) -> FindNodeMessage:
        if enr not in self.tasks:
            # requests are started from bucket #1
            self.tasks[enr] = FindPeersStatus.default()
        return FindNodeMessage(self.tasks[enr].next_distance, self.home)

    def parse(self, nodes: NodesMessage):
        if len(nodes.nodes) == 0:
            return
        current_bucket = log_distance_sim(nodes.sender.id, nodes.nodes[0].id)
        nodes_in_bucket = 0
        task = self.tasks[nodes.sender]
        total_discovered = task.total_discovered
        for node in nodes.nodes:
            node_bucket = log_distance_sim(nodes.sender.id, node.id)
            if node_bucket != current_bucket:
                current_bucket = node_bucket
                nodes_in_bucket = 0
            nodes_in_bucket += 1
            total_discovered += 1
            self.table.put(node)
        next_bucket = current_bucket

        # Last bucket fully dispatched
        if nodes_in_bucket == K:
            next_bucket += 1

        # node tracing is over
        if next_bucket > BUCKETS or task.total_discovered >= MAX_FIND_PEERS:
            del task
        else:
            self.tasks[nodes.sender] = FindPeersStatus(next_bucket, total_discovered)
