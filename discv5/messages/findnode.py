from enr import ENR
from messages.message import Message


class FindNodeMessage(Message):
    distance: int

    def __init__(self, distance: int, sender: ENR) -> None:
        super().__init__(sender)
        self.distance = distance

    def get(self) -> int:
        return self.distance
