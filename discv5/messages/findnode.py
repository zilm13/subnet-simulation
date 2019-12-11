from enr import ENR
from messages.message import Message


class FindNodeMessage(Message):
    distance: int

    def __init__(self, distance: int, sender: ENR) -> None:
        super().__init__(sender)
        self.distance = distance

    def __str__(self) -> str:
        return "FindNodeMessage[" + super().__str__() + ", distance: " + str(self.distance) + "]"
