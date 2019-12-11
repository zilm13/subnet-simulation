from typing import NamedTuple


class ENR(NamedTuple):
    ip: str
    port: int
    id: bytes

    @classmethod
    def from_values(cls, ip: str, port: int, id_: bytes):
        return cls(ip, port, id_)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if self is other:
            return True
        return self.id == other.id

    def __str__(self) -> str:
        return "ENR[ID: " + self.id.hex() + ", Addr: " + self.ip + ":" + str(self.port) + "]"
