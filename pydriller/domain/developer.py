class Developer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __eq__(self, other):
        if not isinstance(other, Developer):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.__dict__ == other.__dict__
