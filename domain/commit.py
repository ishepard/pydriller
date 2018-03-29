from _datetime import datetime
from typing import List
from dateutil import tz
from domain.developer import Developer
from domain.modification import Modification
from domain.modification_type import ModificationType


class Commit:
    def __init__(self, hash: str, author: Developer, committer: Developer,
                 author_date: datetime, committer_date: datetime,
                 author_timezone: tz, committer_timezone: tz,
                 msg: str, parent: str, merge: bool = False, branches: set = set(),
                 is_commit_in_main_branch: bool = False) -> None:
        """
        Create a commit object.
        :param hash: hash of the commit
        :param author: author of the commit
        :param committer: committer of the commit
        :param author_date: date when the author committed
        :param committer_date: date when the committer committed
        :param msg: message of the commit
        :param parent: hash of the parent commit
        :param merge: True if the commit is a merge commit
        :param branches: branches that include the commit
        :param is_commit_in_main_branch: True if the commit is in the main branch
        """
        self.hash = hash
        self.author = author
        self.committer = committer
        self.author_date = author_date
        self.committer_date = committer_date
        self.author_timezone = author_timezone
        self.committer_timezone = committer_timezone
        self.msg = msg
        self.parent = parent
        self.merge = merge
        self.modifications: List[Modification] = []
        self.branches = branches
        self.in_main_branch = is_commit_in_main_branch

    def add_modifications(self, old_path: str, new_path: str, change: ModificationType, diff: str, sc: str):
        """
        Add a modification to the commit.
        :param old_path: old path of the file (can be null if the file is added)
        :param new_path: new path of the file (can be null if the file is deleted)
        :param change: type of the change
        :param diff: diff of the change
        :param sc: source code of the file (can be null if the file is deleted)
        """
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
        return ('Hash: {}'.format(self.hash) + '\n'
                'Author: {}'.format(self.author.name) + '\n'
                'Author email: {}'.format(self.author.email) + '\n'
                'Committer: {}'.format(self.committer.name) + '\n'
                'Committer email: {}'.format(self.committer.email) + '\n'
                'Author date: {}'.format(self.author_date.strftime("%Y-%m-%d %H:%M:%S")) + '\n'
                'Committer date: {}'.format(self.committer_date.strftime("%Y-%m-%d %H:%M:%S")) + '\n'
                'Message: {}'.format(self.msg) + '\n'
                'Parent: {}'.format(self.parent) + '\n'
                'Merge: {}'.format(self.merge) + '\n'
                'Modifications: \n{}'.format("\n".join(map(str, self.modifications))) + '\n'
                'Branches: \n{}'.format("\n".join(map(str, self.branches))) + '\n'
                'In main branch: {}'.format(self.in_main_branch)
                )