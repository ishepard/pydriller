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
from _datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Set, Dict

import lizard
from git import Diff, Git, Commit as GitCommit, NULL_TREE

from pydriller.domain.developer import Developer

logger = logging.getLogger(__name__)


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

    def __init__(self, old_path: str, new_path: str,
                 change_type: ModificationType,
                 diff_and_sc: Dict[str, str]):
        """
        Initialize a modification. A modification carries on information
        regarding the changed file. Normally, you shouldn't initialize a new
        one.
        """
        self._old_path = Path(old_path) if old_path is not None else None
        self._new_path = Path(new_path) if new_path is not None else None
        self.change_type = change_type
        self.diff = diff_and_sc['diff']
        self.source_code = diff_and_sc['source_code']
        self.source_code_before = diff_and_sc['source_code_before']

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
    def old_path(self):
        """
        Old path of the file. Can be None if the file is added.

        :return: str old_path
        """
        if self._old_path is not None:
            return str(self._old_path)
        return None

    @property
    def new_path(self):
        """
        New path of the file. Can be None if the file is deleted.

        :return: str new_path
        """
        if self._new_path is not None:
            return str(self._new_path)
        return None

    @property
    def filename(self) -> str:
        """
        Return the filename. Given a path-like-string (e.g.
        "/Users/dspadini/pydriller/myfile.py") returns only the filename
        (e.g. "myfile.py")

        :return: str filename
        """
        if self._new_path is not None and str(self._new_path) != "/dev/null":
            path = self._new_path
        else:
            path = self._old_path

        return path.name

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
            analysis = lizard.analyze_file.analyze_source_code(self.filename,
                                                               self.source_code
                                                               )

            self._nloc = analysis.nloc
            self._complexity = analysis.CCN
            self._token_count = analysis.token_count

            for func in analysis.function_list:
                self._function_list.append(Method(func))

    def __eq__(self, other):
        if not isinstance(other, Modification):
            return NotImplemented
        if self is other:
            return True
        return self.__dict__ == other.__dict__


class Commit:
    """
    Class representing a Commit. Contains all the important information such
    as hash, author, dates, and modified files.
    """

    def __init__(self, commit: GitCommit, conf) -> None:
        """
        Create a commit object.

        :param commit: GitPython Commit object
        :param conf: Configuration class
        """
        self._c_object = commit

        self._modifications = None
        self._branches = None
        self._conf = conf

    @property
    def hash(self) -> str:
        """
        Return the SHA of the commit.

        :return: str hash
        """
        return self._c_object.hexsha

    @property
    def author(self) -> Developer:
        """
        Return the author of the commit as a Developer object.

        :return: author
        """
        return Developer(self._c_object.author.name,
                         self._c_object.author.email)

    @property
    def committer(self) -> Developer:
        """
        Return the committer of the commit as a Developer object.

        :return: committer
        """
        return Developer(self._c_object.committer.name,
                         self._c_object.committer.email)

    @property
    def project_name(self) -> str:
        """
        Return the project name.

        :return: project name
        """
        return Path(self._conf.get('path_to_repo')).name

    @property
    def author_date(self) -> datetime:
        """
        Return the authored datetime.

        :return: datetime author_datetime
        """
        return self._c_object.authored_datetime

    @property
    def committer_date(self) -> datetime:
        """
        Return the committed datetime.

        :return: datetime committer_datetime
        """
        return self._c_object.committed_datetime

    @property
    def author_timezone(self) -> int:
        """
        Author timezone expressed in seconds from epoch.

        :return: int timezone
        """
        return self._c_object.author_tz_offset

    @property
    def committer_timezone(self) -> int:
        """
        Author timezone expressed in seconds from epoch.

        :return: int timezone
        """
        return self._c_object.committer_tz_offset

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
        parents = []
        for p in self._c_object.parents:
            parents.append(p.hexsha)
        return parents

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
        options = {}
        if self._conf.get('histogram'):
            options['histogram'] = True

        if self._conf.get('skip_whitespaces'):
            options['w'] = True

        if len(self.parents) == 1:
            # the commit has a parent
            diff_index = self._c_object.parents[0].diff(self._c_object,
                                                        create_patch=True,
                                                        **options)
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
            diff_index = []
        else:
            # this is the first commit of the repo. Comparing it with git
            # NULL TREE
            diff_index = self._c_object.diff(NULL_TREE,
                                             create_patch=True,
                                             **options)

        return self._parse_diff(diff_index)

    def _parse_diff(self, diff_index) -> List[Modification]:
        modifications_list = []
        for diff in diff_index:
            old_path = diff.a_path
            new_path = diff.b_path
            change_type = self._from_change_to_modification_type(diff)

            diff_and_sc = {
                'diff': self._get_decoded_str(diff.diff),
                'source_code_before': self._get_decoded_sc_str(
                    diff.a_blob),
                'source_code': self._get_decoded_sc_str(
                    diff.b_blob)
            }

            modifications_list.append(Modification(old_path, new_path,
                                                   change_type, diff_and_sc))

        return modifications_list

    def _get_decoded_str(self, diff):
        try:
            return diff.decode('utf-8', 'ignore')
        except (UnicodeDecodeError, AttributeError, ValueError):
            logger.debug('Could not load the diff of a '
                         'file in commit %s', self._c_object.hexsha)
            return None

    def _get_decoded_sc_str(self, diff):
        try:
            return diff.data_stream.read().decode('utf-8', 'ignore')
        except (UnicodeDecodeError, AttributeError, ValueError):
            logger.debug('Could not load source code of a '
                         'file in commit %s', self._c_object.hexsha)
            return None

    @property
    def in_main_branch(self) -> bool:
        """
        Return True if the commit is in the main branch, False otherwise.

        :return: bool in_main_branch
        """
        return self._conf.get('main_branch') in self.branches

    @property
    def branches(self) -> Set[str]:
        """
        Return the set of branches that contain the commit.

        :return: set(str) branches
        """
        if self._branches is None:
            self._branches = self._get_branches()

        return self._branches

    def _get_branches(self):
        c_git = Git(str(self._conf.get('path_to_repo')))
        branches = set()
        for branch in set(c_git.branch('--contains', self.hash).split('\n')):
            branches.add(branch.strip().replace('* ', ''))
        return branches

    # pylint disable=R0902
    @staticmethod
    def _from_change_to_modification_type(diff: Diff):
        if diff.new_file:
            return ModificationType.ADD
        if diff.deleted_file:
            return ModificationType.DELETE
        if diff.renamed_file:
            return ModificationType.RENAME
        if diff.a_blob and diff.b_blob and diff.a_blob != diff.b_blob:
            return ModificationType.MODIFY

        return ModificationType.UNKNOWN

    def __eq__(self, other):
        if not isinstance(other, Commit):
            return NotImplemented
        if self is other:
            return True

        return self.__dict__ == other.__dict__
