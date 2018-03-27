from _datetime import datetime
from domain.developer import Developer
from domain.modification import Modification
from domain.modification_type import ModificationType


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
        self.modifications = []
        self.branches = branches
        self.in_main_branch = isCommitInMainBranch

    def add_modifications(self, old_path: str, new_path: str, change: ModificationType, diff: str, sc: str):
        m = Modification(old_path, new_path, change, diff, sc)
        self.modifications.append(m)

    def __eq__(self, other):
        if not isinstance(other, Commit):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return ('Hash: ' + self.hash + '\n'
                'Author: ' + self.author.name + '\n'
                'Author email: ' + self.author.email + '\n'
                'Committer: ' + self.committer.name + '\n'
                'Committer email: ' + self.committer.email + '\n'
                'Date: ' + self.date.strftime("%Y-%m-%d %H:%M:%S") + '\n'
                'Committer date: ' + self.committer_date.strftime("%Y-%m-%d %H:%M:%S") + '\n'
                'Message: ' + self.msg + '\n'
                'Parent: ' + self.parent + '\n'
                'Merge: ' + str(self.merge) + '\n'
                'Modifications: ' + "\n".join(map(str, self.modifications)) + '\n'
                'Branches: ' "\n".join(map(str, self.branches)) + '\n'
                'In main branch: {}'.format(self.in_main_branch)
                )