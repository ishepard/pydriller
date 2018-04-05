class Developer:
    def __init__(self, name: str, email: str):
        """
        Class to identify a developer.

        :param str name: name and surname of the developer
        :param str email: email of the developer
        """
        self.name = name
        self.email = email

    def __eq__(self, other):
        if not isinstance(other, Developer):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.__dict__ == other.__dict__
