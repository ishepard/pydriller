class BlamedLine:
    def __init__(self, line_number: int, line: str, author: str, committer: str, commit: str):
        self.line_number = line_number
        self.line = line
        self.author = author
        self.committer = committer
        self.commit = commit

    def __eq__(self, other):
        if not isinstance(other, BlamedLine):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.__dict__ == other.__dict__

