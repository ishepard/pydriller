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

"""
This module contains all the classes regarding a specific commit, such as
Commit, Modification,
ModificationType and Method.
"""

import logging
from datetime import datetime, timezone, timedelta
from pygit2 import Commit as PyCommit, Repository as PyRepo
from typing import List, Generator

from pydriller.domain.developer import Developer
from pydriller.domain.commit import Commit, Modification, ModificationType

logger = logging.getLogger(__name__)


class CommitPG2(Commit):
    """
    Class representing a Commit. Contains all the important information such
    as hash, author, dates, and modified files.
    """

    def __init__(self, commit: PyCommit, conf) -> None:
        """
        Create a commit object.

        :param commit: GitGP Commit object
        :param project_path: path to the project (temporary folder in case
            of a remote repository)
        :param main_branch: main branch of the repo
        """
        super().__init__(commit, conf)

    @property
    def hash(self) -> str:
        """
        Return the SHA of the commit.

        :return: str hash
        """
        return self._c_object.hex

    @property
    def author(self) -> Developer:
        """
        Return the author of the commit as a Developer object.

        :return: author
        """
        return Developer(self._c_object.author.name,
                         self._c_object.author.email)

    @property
    def author_date(self) -> datetime:
        """
        Return the authored datetime.

        :return: datetime author_datetime
        """
        offset = self._c_object.author.offset * 60
        dt = datetime.utcfromtimestamp(self._c_object.author.time) + \
             timedelta(seconds=offset)
        return dt.replace(tzinfo=timezone(timedelta(seconds=offset)))

    @property
    def author_timezone(self) -> int:
        """
        Author timezone expressed in seconds from epoch.

        :return: int timezone
        """
        return self._c_object.author.offset

    @property
    def committer(self) -> Developer:
        """
        Return the committer of the commit as a Developer object.

        :return: committer
        """
        return Developer(self._c_object.committer.name,
                         self._c_object.committer.email)

    @property
    def committer_date(self) -> datetime:
        """
        Return the committed datetime.

        :return: datetime committer_datetime
        """
        offset = self._c_object.commit_time_offset * 60
        dt = datetime.utcfromtimestamp(self._c_object.commit_time) + \
             timedelta(seconds=offset)
        return dt.replace(tzinfo=timezone(timedelta(seconds=offset)))

    @property
    def committer_timezone(self) -> int:
        """
        Author timezone expressed in seconds from epoch.

        :return: int timezone
        """
        return self._c_object.commit_time_offset

    @property
    def msg(self) -> str:
        """
        Return commit message.

        :return: str commit_message
        """
        return self._c_object.message.strip()

    @property
    def parents(self):
        """
        Return a generator with the parents' commits.

        :return: List[str] parents
        """
        parents = []
        for parent in self._c_object.parents:
            parents.append(Commit(parent, self._conf))

        return parents

    @property
    def merge(self) -> bool:
        """
        Return True if the commit is a merge, False otherwise.

        :return: bool merge
        """
        return len(self._c_object.parents) > 1

    @property
    def modifications(self) -> Generator[Modification, None, None]:
        """
        Return a generator of modified files.

        :return: Generator[Modification, None, None] modifications
        """
        num_parents = len(self.parents)
        if num_parents == 1:
            # the commit has a parent
            diff = self._repo.diff(self._c_object.parents[0].hex,
                                   self._c_object.hex)
            diff.find_similar()
        elif num_parents > 1:
            # if it's a merge commit, the modified files of the commit are the
            # conflicts. This because if the file is not in conflict,
            # pydriller will visit the modification in one of the previous
            # commits. However, parsing the output of a combined diff (that
            # returns the list of conflicts) is challenging: so, right now,
            # I will return an empty array, in the meanwhile I will try to
            # find a way to parse the output.
            # c_git = Git(str(self.project_path))
            # d = c_git.diff_tree("--cc", commit.hexsha, '-r', '--abbrev=40',
            #                     '--full-index', '-M', '-p', '--no-color')
            diff = []
        else:
            # this is the first commit of the repo. Comparing it with git
            # NULL TREE
            diff = self._c_object.tree.diff_to_tree(swap=True)
            diff.find_similar()

        for patch in diff:
            yield Modification(patch, self._repo, self._c_object)

    @property
    def in_main_branch(self) -> bool:
        """
        Return True if the commit is in the main branch, False otherwise.

        :return: bool in_main_branch
        """
        return self._main_branch in self.branches

    @property
    def branches(self) -> List[str]:
        """
        Return the set of branches that contain the commit.

        :return: set(str) branches
        """
        if self._branches is None:
            self._branches = self._get_branches()

        return self._branches

    def _get_branches(self):
        return list(self._repo.branches.with_commit(self.hash))

    def __eq__(self, other):
        if not isinstance(other, Commit):
            return NotImplemented
        if self is other:
            return True

        return self.__dict__ == other.__dict__