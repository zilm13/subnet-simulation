from enr import ENR
from messages.message import Message


class FindNodeMessage(Message):
    sender: ENR
    distance: int

    def __init__(self, distance: int, sender: ENR) -> None:
        self.distance = distance
        self.sender = sender

    def get(self) -> int:
        return self.distance

    def sender(self) -> ENR:
        return self.sender
