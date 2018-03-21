from _datetime import datetime
from domain.Developer import Developer
from domain.Modification import Modification
from domain.ModificationType import ModificationType


class Commit:
    def __init__(self, hash: str, author: Developer, committer: Developer, author_date: datetime, committer_date: datetime, msg: str, parent: str, merge: bool = False, branches: set = set(), isCommitInMainBranch: bool = False):
        self.hash = hash
        self.author = author
        self.committer = committer
        self.date = author_date
        self.committer_date = committer_date
        self.msg = msg
        self.parent = parent
        self.merge = merge
        self.modifications = [Modification]
        self.branches = branches
        self.in_main_branch = isCommitInMainBranch

    def add_modifications(self, old_path: str, new_path: str, change: ModificationType, diff: str, sc: str):
        m = Modification(old_path, new_path, change, diff, sc)
        self.modifications.append(m)

    def add_modifications(self, modifications: []):
        self.modifications.extend(modifications)

    def __eq__(self, other):
        if not isinstance(other, Commit):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.__dict__ == other.__dict__
