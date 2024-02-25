from datetime import datetime


class Message:
    def __init__(self, message, sender, id=None):
        self.id = id or str(datetime.utcnow().timestamp() * 1000)
        self.message = message
        self.sender = sender

    def __hash__(self):
        return hash((self.id, self.message, self.sender))

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return (self.id, self.message, self.sender) == (other.id, other.message, other.sender)

    def __str__(self):
        return f"Message(id={self.id}, message={self.message}, sender={self.sender})"
