from typing import NamedTuple, Iterable, Tuple, Any


class ENR(NamedTuple):
    ip: str
    port: int
    id: bytes

    def __init__(self, ip: str, port: int, id: bytes) -> None:
        self.ip = ip
        self.port = port
        self.id = id

    def __eq__(self, other):
        """Overrides the default implementation"""
        if self == other:
            return True
        return self.id == other.id
