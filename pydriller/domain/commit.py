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
from enum import Enum
from pathlib import Path
from typing import List, Set, Dict

import lizard
from git import Repo, Diff, Git, Commit as GitCommit

logger = logging.getLogger(__name__)
from pydriller.domain.developer import Developer

NULL_TREE = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'


class ModificationType(Enum):
    ADD = 1,
    COPY = 2,
    RENAME = 3,
    DELETE = 4,
    MODIFY = 5,
    UNKNOWN = 6


class Method:
    def __init__(self, func):
        """
        Initialize a method object. This is calculated using Lizard: it parses
        the source code of all the modifications in a commit, extracting information
        of the methods contained in the file (if the file is a source code written
        in one of the supported programming languages).
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


class Modification:
    def __init__(self, old_path: str, new_path: str,
                 change_type: ModificationType,
                 diff_and_sc: Dict[str, str]):
        """
        Initialize a modification. A modification carries on information regarding
        the changed file. Normally, you shouldn't initialize a new one.
        """
        self._old_path = Path(old_path) if old_path is not None else None
        self._new_path = Path(new_path) if new_path is not None else None
        self.change_type = change_type
        self.diff = diff_and_sc['diff']
        self.source_code = diff_and_sc['source_code']

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
        if self._old_path:
            return str(self._old_path)
        return self._old_path

    @property
    def new_path(self):
        """
        New path of the file. Can be None if the file is deleted.

        :return: str new_path
        """
        if self._new_path:
            return str(self._new_path)
        return self._new_path

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
            l = lizard.analyze_file.analyze_source_code(self.filename, self.source_code)

            self._nloc = l.nloc
            self._complexity = l.CCN
            self._token_count = l.token_count

            for func in l.function_list:
                self._function_list.append(Method(func))

    def __eq__(self, other):
        if not isinstance(other, Modification):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return (
                'MODIFICATION\n' +
                'Old Path: {}\n'.format(self.old_path) +
                'New Path: {}\n'.format(self.new_path) +
                'Type: {}\n'.format(self.change_type.name) +
                'Diff: {}\n'.format(self.diff) +
                'Source code: {}\n'.format(self.source_code)
        )


class Commit:
    def __init__(self, commit: GitCommit, project_path: Path, main_branch: str) -> None:
        """
        Create a commit object.

        :param commit: GitPython Commit object
        :param project_path: path to the project (temporary folder in case of a remote repository)
        :param main_branch: main branch of the repo
        """
        self._c_object = commit
        self._main_branch = main_branch
        self.project_path = project_path

        self._modifications = None
        self._branches = None

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
        return Developer(self._c_object.author.name, self._c_object.author.email)

    @property
    def committer(self) -> Developer:
        """
        Return the committer of the commit as a Developer object.

        :return: committer
        """
        return Developer(self._c_object.committer.name, self._c_object.committer.email)

    @property
    def project_name(self) -> str:
        """
        Return the project name.

        :return: project name
        """
        return self.project_path.name

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
        repo = Repo(str(self.project_path))
        commit = self._c_object

        if len(self.parents) > 0:
            # the commit has a parent
            diff_index = self._c_object.parents[0].diff(commit, create_patch=True)
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

            diff_and_sc = {
                'diff': '',
                'source_code': ''
            }

            try:
                diff_and_sc['diff'] = d.diff.decode('utf-8')
                diff_and_sc['source_code'] = d.b_blob.data_stream.read().decode('utf-8')
            except (UnicodeDecodeError, AttributeError, ValueError):
                logger.debug(
                    'Could not load source code or the diff of a file in commit {}'.format(self._c_object.hexsha))

            modifications_list.append(Modification(old_path, new_path, change_type, diff_and_sc))

        return modifications_list

    @property
    def in_main_branch(self) -> bool:
        """
        Return True if the commit is in the main branch, False otherwise.

        :return: bool in_main_branch
        """
        return self._main_branch in self.branches

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
        git = Git(str(self.project_path))
        branches = set()
        for branch in set(git.branch('--contains', self.hash).split('\n')):
            branches.add(branch.strip().replace('* ', ''))
        return branches

    def _from_change_to_modification_type(self, d: Diff):
        if d.new_file:
            return ModificationType.ADD
        elif d.deleted_file:
            return ModificationType.DELETE
        elif d.renamed_file:
            return ModificationType.RENAME
        elif d.a_blob and d.b_blob and d.a_blob != d.b_blob:
            return ModificationType.MODIFY
        else:
            return ModificationType.UNKNOWN

    def __eq__(self, other):
        if not isinstance(other, Commit):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return ('Hash: {}\n'.format(self.hash) +
                'Author: {}\n'.format(self.author.name) +
                'Author email: {}\n'.format(self.author.email) +
                'Committer: {}\n'.format(self.committer.name) +
                'Committer email: {}\n'.format(self.committer.email) +
                'Author date: {}\n'.format(self.author_date.strftime("%Y-%m-%d %H:%M:%S")) +
                'Committer date: {}\n'.format(self.committer_date.strftime("%Y-%m-%d %H:%M:%S")) +
                'Message: {}\n'.format(self.msg) +
                'Parent: {}\n'.format("\n".join(map(str, self.parents))) +
                'Merge: {}\n'.format(self.merge) +
                'Modifications: \n{}'.format("\n".join(map(str, self.modifications))) +
                'Branches: \n{}'.format("\n".join(map(str, self.branches))) +
                'In main branch: {}\n'.format(self.in_main_branch)
                )
