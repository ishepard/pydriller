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
import logging
from _datetime import datetime
from typing import List

from git import Repo, Diff

logger = logging.getLogger(__name__)
from pydriller.domain.developer import Developer
from pydriller.domain.modification import Modification, ModificationType

NULL_TREE = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'


class Commit:
    def __init__(self, hash: str, author: Developer, committer: Developer,
                 author_date: datetime, committer_date: datetime,
                 author_timezone: int, committer_timezone: int,
                 msg: str, parents: List[str], merge: bool = False, branches: set = set(),
                 is_commit_in_main_branch: bool = False, path: str = None) -> None:
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
        self.branches = branches
        self.in_main_branch = is_commit_in_main_branch
        self.path = path

    @property
    def modifications(self):
        repo = Repo(self.path)
        commit = repo.commit(self.hash)

        if len(self.parents) > 0:
            # the commit has a parent
            parent = repo.commit(self.parents[0])
            diff_index = parent.diff(commit, create_patch=True)
        else:
            # this is the first commit of the repo. Comparing it with git NULL TREE
            parent = repo.tree(NULL_TREE)
            diff_index = parent.diff(commit.tree, create_patch=True)

        return self._parse_diff(diff_index)

    def _parse_diff(self, diff_index) -> List[Modification]:
        modifications_list = []
        for d in diff_index:
            old_path = d.a_path
            new_path = d.b_path
            change_type = self._from_change_to_modification_type(d)
            sc = ''
            diff_text = ''
            try:
                sc = d.b_blob.data_stream.read().decode('utf-8')
                diff_text = d.diff.decode('utf-8')
            except (UnicodeDecodeError, AttributeError, ValueError):
                logger.debug('Could not load source code or the diff of a file in commit {}'.format(self.hash))

            modifications_list.append(Modification(old_path, new_path, change_type, diff_text, sc))
        return modifications_list

    def _from_change_to_modification_type(self, d: Diff):
        if d.new_file:
            return ModificationType.ADD
        elif d.deleted_file:
            return ModificationType.DELETE
        elif d.renamed_file:
            return ModificationType.RENAME
        elif d.a_blob and d.b_blob and d.a_blob != d.b_blob:
            return ModificationType.MODIFY

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