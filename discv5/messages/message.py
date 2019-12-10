from enr import ENR


class Message(object):
    sender: ENR

    def __init__(self, sender: ENR) -> None:
        self.sender = sender
