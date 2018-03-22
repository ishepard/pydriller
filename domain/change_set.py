from datetime import datetime


class ChangeSet:
    def __init__(self, id: str, date: datetime):
        self.id = id
        self.date = date

    def __eq__(self, other):
        if not isinstance(other, ChangeSet):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.__dict__ == other.__dict__
