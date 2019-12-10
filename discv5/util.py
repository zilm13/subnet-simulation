from math import ceil
from config import DISTANCE_DIVISOR

# Default id size we respect to
ID_SIZE = 32


def big_endian_to_int(value: bytes) -> int:
    return int.from_bytes(value, "big")


# discv5 like distance
def log_distance(id1: bytes, id2: bytes) -> int:
    assert len(id1) == ID_SIZE
    assert len(id2) == ID_SIZE
    left_int = big_endian_to_int(id1)
    right_int = big_endian_to_int(id2)
    diff = left_int ^ right_int
    return diff.bit_length()


# Simplified distance to reduce number of distances for simulation
def log_distance_sim(id1: bytes, id2: bytes) -> int:
    return ceil(log_distance(id1, id2) / DISTANCE_DIVISOR)
