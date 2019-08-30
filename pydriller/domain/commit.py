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
from enum import Enum
from pathlib import Path
from pygit2 import Commit as PyCommit, Repository as PyRepo
from typing import List, Set
# from pympler import asizeof
import lizard

from pydriller.domain.developer import Developer

logger = logging.getLogger(__name__)

NULL_TREE = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'


class ModificationType(Enum):
    """
    Type of Modification. Can be ADD, COPY, RENAME, DELETE, MODIFY or UNKNOWN.
    """

    ADD = 1
    COPY = 2
    RENAME = 3
    DELETE = 4
    MODIFY = 5
    UNKNOWN = 6


class Method:  # pylint: disable=R0902
    """
    This class represents a method in a class. Contains various information
    extracted through Lizard.
    """

    def __init__(self, func):
        """
        Initialize a method object. This is calculated using Lizard: it parses
        the source code of all the modifications in a commit, extracting
        information of the methods contained in the file (if the file is a
        source code written in one of the supported programming languages).
        """

        self.name = func.name
        self.long_name = func.long_name
        self.filename = func.filename
        self.nloc = func.nloc
        self.complexity = func.cyclomatic_complexity
        self.token_count = func.token_count
        self.parameters = func.parameters
        self.start_line = func.start_line
        self.end_line = func.end_line
        self.fan_in = func.fan_in
        self.fan_out = func.fan_out
        self.general_fan_out = func.general_fan_out
        self.length = func.length
        self.top_nesting_level = func.top_nesting_level


class Modification:  # pylint: disable=R0902
    """
    This class contains information regarding a modified file in a commit.
    """

    def __init__(self, patch, repo: PyRepo, commit: PyCommit):
        """
        Initialize a modification. A modification carries on information
        regarding the changed file. Normally, you shouldn't initialize a new
        one.
        """
        self._old_path = None
        self._new_path = None
        self._change_type = None
        self._patch = patch
        self._delta = patch.delta

        # to get the source code we need the repo and commit object
        self._repo = repo
        self._commit = commit

        # expensive to calculate, so I calculate them only once and then I
        # save them in a temporary field
        self._diff = None
        self._source_code = None
        self._source_code_before = None

        # fields we get back from Lizard
        self._nloc = None
        self._complexity = None
        self._token_count = None
        self._function_list = []

    @property
    def added(self) -> int:
        """
        Return the total number of added lines in the file.

        :return: int lines_added
        """
        added = 0
        for line in self.diff.replace('\r', '').split("\n"):
            if line.startswith('+') and not line.startswith('+++'):
                added += 1
        return added

    @property
    def removed(self):
        """
        Return the total number of deleted lines in the file.

        :return: int lines_deleted
        """
        removed = 0
        for line in self.diff.replace('\r', '').split("\n"):
            if line.startswith('-') and not line.startswith('---'):
                removed += 1
        return removed

    @property
    def old_path(self) -> Path:
        """
        Old path of the file. Can be None if the file is added.

        :return: str old_path
        """
        if self._old_path is None and self.change_type != ModificationType.ADD:
            self._old_path = Path(self._delta.old_file.path)
        return self._old_path

    @property
    def new_path(self) -> Path:
        """
        New path of the file. Can be None if the file is deleted.

        :return: str new_path
        """
        if self._new_path is None and self.change_type != ModificationType.DELETE:
            self._new_path = Path(self._delta.new_file.path)
        return self._new_path

    @property
    def change_type(self) -> ModificationType:
        if self._change_type is None:
            self._change_type = self._from_change_to_modification_type(
                self._delta.status_char())
        return self._change_type

    @property
    def filename(self) -> str:
        """
        Return the filename. Given a path-like-string (e.g.
        "/Users/dspadini/pydriller/myfile.py") returns only the filename
        (e.g. "myfile.py")

        :return: str filename
        """
        if self.new_path is not None and str(self.new_path) != "/dev/null":
            path = self.new_path
        else:
            path = self.old_path

        return path.name

    @property
    def diff(self) -> str:
        if self._diff is None:
            self._diff = self._patch.data.decode('utf-8', 'ignore')
        return self._diff

    @property
    def source_code(self) -> str:
        if self._source_code is None and self.change_type != \
                ModificationType.DELETE:
            self._source_code = self._repo[self._commit.tree[
                str(self.new_path)].id].data.decode('utf-8', 'ignore')
        # print(f'Commit after mod size is {asizeof.asizeof(self)}')
        return self._source_code

    @property
    def source_code_before(self) -> str:
        if self._source_code_before is None and self.change_type != \
                ModificationType.ADD:
            self._source_code_before = self._repo[self._commit.parents[0].tree[
                str(self.old_path)].id].data.decode('utf-8', 'ignore')
        return self._source_code_before

    # pylint disable=R0902
    def _from_change_to_modification_type(self, diff_char: str) -> \
            ModificationType:
        if diff_char == 'A':
            return ModificationType.ADD
        if diff_char == 'D':
            return ModificationType.DELETE
        if diff_char == 'R':
            return ModificationType.RENAME
        if diff_char == 'M':
            return ModificationType.MODIFY

        return ModificationType.UNKNOWN

    @property
    def nloc(self) -> int:
        """
        Calculate the LOC of the file.

        :return: LOC of the file
        """
        self._calculate_metrics()
        return self._nloc

    @property
    def complexity(self) -> int:
        """
        Calculate the Cyclomatic Complexity of the file.

        :return: Cyclomatic Complexity of the file
        """
        self._calculate_metrics()
        return self._complexity

    @property
    def token_count(self) -> int:
        """
        Calculate the token count of functions.

        :return: token count
        """
        self._calculate_metrics()
        return self._token_count

    @property
    def methods(self) -> List[Method]:
        """
        Return the list of methods in the file. Every method
        contains various information like complexity, loc, name,
        number of parameters, etc.

        :return: list of methods
        """
        self._calculate_metrics()
        return self._function_list

    def _calculate_metrics(self):
        if self.source_code and self._nloc is None:
            l = lizard.analyze_file.analyze_source_code(self.filename,
                                                        self.source_code)

            self._nloc = l.nloc
            self._complexity = l.CCN
            self._token_count = l.token_count

            for func in l.function_list:
                self._function_list.append(Method(func))

    def __eq__(self, other):
        if not isinstance(other, Modification):
            return NotImplemented
        if self._commit.hex == other._commit.hex and self._repo.path == \
                other._repo.path:
            return True
        return self.__dict__ == other.__dict__


class Commit:
    """
    Class representing a Commit. Contains all the important information such
    as hash, author, dates, and modified files.
    """

    def __init__(self, commit: PyCommit, repo: PyRepo, project_path: Path,
                 main_branch: str) -> None:
        """
        Create a commit object.

        :param commit: GitPython Commit object
        :param project_path: path to the project (temporary folder in case
            of a remote repository)
        :param main_branch: main branch of the repo
        """
        self._c_object = commit
        self._main_branch = main_branch
        self.project_path = project_path
        self._repo = repo
        self._modifications = None
        self._branches = None

    @property
    def hash(self) -> str:
        """
        Return the SHA of the commit.

        :return: str hash
        """
        return self._c_object.hex

    @property
    def project_name(self) -> str:
        """
        Return the project name.

        :return: project name
        """
        return self.project_path.name

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
    def parents(self) -> List[str]:
        """
        Return the list of parents SHAs.

        :return: List[str] parents
        """
        return [str(p) for p in self._c_object.parent_ids]

    @property
    def merge(self) -> bool:
        """
        Return True if the commit is a merge, False otherwise.

        :return: bool merge
        """
        return len(self._c_object.parents) > 1

    @property
    def modifications(self) -> List[Modification]:
        """
        Return a list of modified files.

        :return: List[Modification] modifications
        """
        if self._modifications is None:
            self._modifications = self._get_modifications()
        return self._modifications

    def _get_modifications(self):
        if len(self.parents) == 1:
            # the commit has a parent
            diff = self._repo.diff(self._c_object.parents[0].hex,
                                   self._c_object.hex)
            diff.find_similar()
        elif len(self.parents) > 1:
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

        return self._parse_diff(diff)

    def _parse_diff(self, diff) -> List[Modification]:
        modifications_list = []
        for patch in diff:
            modifications_list.append(Modification(patch, self._repo,
                                                   self._c_object))

        return modifications_list

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
