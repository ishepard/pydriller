# Copyright 2018 Davide Spadini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from _datetime import datetime
from typing import List
from pydriller.domain.developer import Developer
from pydriller.domain.modification import Modification, ModificationType


class Commit:
    def __init__(self, hash: str, author: Developer, committer: Developer,
                 author_date: datetime, committer_date: datetime,
                 author_timezone: int, committer_timezone: int,
                 msg: str, parents: List[str], merge: bool = False, branches: set = set(),
                 is_commit_in_main_branch: bool = False) -> None:
        """
        Create a commit object.

        :param str hash: hash of the commit
        :param Developer author: author of the commit
        :param Developer committer: committer of the commit
        :param datetime author_date: date when the author committed
        :param datetime committer_date: date when the committer committed
        :param int author_timezone: seconds west from UTC
        :param int committer_timezone: seconds west from UTC
        :param str msg: message of the commit
        :param List[str] parents: list of hashes of the parent commits
        :param bool merge: True if the commit is a merge commit
        :param set branches: branches that include the commit
        :param bool is_commit_in_main_branch: True if the commit is in the main branch
        """
        self.hash = hash
        self.author = author
        self.committer = committer
        self.author_date = author_date
        self.committer_date = committer_date
        self.author_timezone = author_timezone
        self.committer_timezone = committer_timezone
        self.msg = msg
        self.parents = parents
        self.merge = merge
        self.modifications = []  # type: List[Modification]
        self.branches = branches
        self.in_main_branch = is_commit_in_main_branch

    def add_modifications(self, old_path: str, new_path: str, change: ModificationType, diff: str, sc: str):
        """
        Add a modification to the commit.

        :param str old_path: old path of the file (can be null if the file is added)
        :param str new_path: new path of the file (can be null if the file is deleted)
        :param ModificationType change: type of the change
        :param str diff: diff of the change
        :param str sc: source code of the file (can be null if the file is deleted)
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
                'Parent: {}'.format("\n".join(map(str, self.parents))) + '\n'
                'Merge: {}'.format(self.merge) + '\n'
                'Modifications: \n{}'.format("\n".join(map(str, self.modifications))) + '\n'
                'Branches: \n{}'.format("\n".join(map(str, self.branches))) + '\n'
                'In main branch: {}'.format(self.in_main_branch)
                )


class ChangeSet:
    def __init__(self, id: str, date: datetime):
        """
        Light-weight version of the commit, storing only the hash and the date. Used for filter out
        commits before asking for more complex information (like diff and source code).

        :param str id: hash of the commit
        :param date: date of the commit
        """
        self.id = id
        self.date = date

    def __eq__(self, other):
        if not isinstance(other, ChangeSet):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.__dict__ == other.__dict__