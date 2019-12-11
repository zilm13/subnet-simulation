from enr import ENR


class Message(object):
    sender: ENR

    def __init__(self, sender: ENR) -> None:
        self.sender = sender

    def __str__(self) -> str:
        # class is used as abstract so not including name etc
        return "sender: " + str(self.sender)
