import logging
from typing import List

from config import (K, BUCKETS, MAX_FIND_PEERS)
from enr import ENR
from kademlia_table import KademliaTable
from messages.findnode import FindNodeMessage
from util import log_distance_sim


class FindPeersTask():
    sender: ENR
    recipient: ENR
    table: KademliaTable
    next_distance: int
    total_discovered: int
    logger: logging.Logger

    def __init__(self, sender: ENR, recipient: ENR, table: KademliaTable):
        self.sender = sender
        self.recipient = recipient
        self.table = table
        self.next_distance = 1
        self.total_discovered = 0
        self.logger = logging.getLogger(__name__)

    def __iter__(self):
        return self

    def __next__(self):
        if self.has_next():
            return FindNodeMessage(self.next_distance, self.sender)
        else:
            raise StopIteration

    def has_next(self) -> bool:
        return self.next_distance < BUCKETS and self.total_discovered < MAX_FIND_PEERS

    def parse(self, nodes: List[ENR]):
        if len(nodes) == 0:
            return
        current_bucket = log_distance_sim(self.recipient.id, nodes[0].id)
        nodes_in_bucket = 0
        total_discovered = self.total_discovered
        for node in nodes:
            node_bucket = log_distance_sim(self.recipient.id, node.id)
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
        # Saving
        if next_bucket > self.next_distance:
            self.next_distance = next_bucket
        self.total_discovered = total_discovered
