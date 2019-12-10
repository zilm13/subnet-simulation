from collections import deque
from typing import (Deque, Dict, List)

from config import (K, BUCKETS)
from enr import ENR
from util import log_distance_sim


class Bucket():
    payload: Deque[ENR]

    def __init__(self) -> None:
        self.payload = deque(maxlen=K)

    def __len__(self) -> int:
        return len(self.payload)

    def __contains__(self, key):
        return key in self.payload

    def put(self, enr: ENR):
        if enr in self.payload:
            self.payload.remove(enr)
        self.payload.append(enr)

    def get(self, index: int) -> ENR:
        return self.payload[index]


class KademliaTable():
    home: ENR
    buckets: Dict[int, Deque]

    def __init__(self, home: ENR, boot_nodes: List[ENR] = None) -> None:
        self.home = home
        self.buckets = dict()
        if boot_nodes is not None:
            for node in boot_nodes:
                self.put(node)

    def put(self, enr: ENR):
        if self.home == enr:
            return
        distance = log_distance_sim(self.home.id, enr.id)
        if distance not in self.buckets:
            self.buckets[distance] = Bucket()
        self.buckets[distance].put(enr)

    def find(self, start_bucket: int, limit: int = K) -> List[ENR]:
        total = 0
        current_bucket = start_bucket
        result = list()
        while total < limit and current_bucket <= BUCKETS:
            if current_bucket in self.buckets:
                needed = min(limit - len(result), len(self.buckets[current_bucket]))
                for i in range(0, needed):
                    result.append(self.buckets[current_bucket].get(i))
                    total += 1
            current_bucket += 1
        return result

    def find_strict(self, bucket: int) -> List[ENR]:
        result = list()
        if bucket in self.buckets:
            for i in range(0, len(self.buckets[bucket])):
                result.append(self.buckets[bucket].get(i))
        return result
