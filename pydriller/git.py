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
This module includes 1 class, GitGP, representing a repository in GitGP.
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Set, Generator

from git import Git as GGitPython, Repo, GitCommandError, Commit as GitCommit

from pydriller.domain.commit import Commit, ModificationType, Modification
from pydriller.utils.common import get_files
from pydriller.utils.conf import Conf

logger = logging.getLogger(__name__)


class Git(ABC):
    """
    Class representing a repository in GitGP. It contains most of the logic of
    PyDriller: obtaining the list of commits, checkout, reset, etc.
    """

    def __init__(self, path: str, conf=None):
        """
        Init the GitGP Repository.

        :param str path: path to the repository
        """
        self.path = Path(path).expanduser().resolve()
        self.project_name = self.path.name

        self._git = None
        self._repo = None

        # if no configuration is passed, then creates a new "emtpy" one
        # with just "path_to_repo" inside.
        if conf is None:
            conf = Conf({
                "path_to_repo": str(self.path),
                "git_repo": self
            })

        self._conf = conf
        self._conf.set_value("main_branch", None)  # init main_branch to None

    @abstractmethod
    def get_head(self) -> Commit:
        pass

    @abstractmethod
    def get_list_commits(self, rev='HEAD', **kwargs) -> Generator[Commit, None, None]:
        pass

    @abstractmethod
    def get_commit(self, commit_id: str) -> Commit:
        pass

    @abstractmethod
    def checkout(self, _hash: str) -> None:
        pass

    @abstractmethod
    def files(self) -> List[str]:
        pass

    @abstractmethod
    def total_commits(self) -> int:
        pass

    @abstractmethod
    def get_commit_from_tag(self, tag: str) -> Commit:
        pass

    @abstractmethod
    def get_tagged_commits(self):
        pass

    def get_commits_last_modified_lines(self, commit: Commit,
                                        modification: Modification = None,
                                        hashes_to_ignore_path: str = None) \
            -> Dict[str, Set[str]]:
        """
        Given the Commit object, returns the set of commits that last
        "touched" the lines that are modified in the files included in the
        commit. It applies SZZ.

        The algorithm works as follow: (for every file in the commit)

        1- obtain the diff

        2- obtain the list of deleted lines

        3- blame the file and obtain the commits were those lines were added

        Can also be passed as parameter a single Modification, in this case
        only this file will be analyzed.

        :param Commit commit: the commit to analyze
        :param Modification modification: single modification to analyze
        :param str hashes_to_ignore_path: path to a file containing hashes of
               commits to ignore.
        :return: the set containing all the bug inducing commits
        """
        if modification is not None:
            modifications = [modification]
        else:
            modifications = commit.modifications

        return self._calculate_last_commits(commit, modifications,
                                            hashes_to_ignore_path)

    def _calculate_last_commits(self, commit: Commit,
                                modifications: List[Modification],
                                hashes_to_ignore_path: str = None) \
            -> Dict[str, Set[str]]:

        commits = {}  # type: Dict[str, Set[str]]

        for mod in modifications:
            path = mod.new_path
            if mod.change_type == ModificationType.RENAME or mod.change_type == ModificationType.DELETE:
                path = mod.old_path
            deleted_lines = mod.diff_parsed['deleted']

            try:
                blame = self._get_blame(commit.hash, path, hashes_to_ignore_path)
                for num_line, line in deleted_lines:
                    if not self._useless_line(line.strip()):
                        buggy_commit = blame[num_line - 1].split(' ')[0].replace('^', '')

                        # Skip unblamable lines.
                        if buggy_commit.startswith("*"):
                            continue

                        if mod.change_type == ModificationType.RENAME:
                            path = mod.new_path

                        commits.setdefault(path, set()).add(self.get_commit(buggy_commit).hash)
            except GitCommandError:
                logger.debug(
                    "Could not found file %s in commit %s. Probably a double "
                    "rename!", mod.filename, commit.hash)

        return commits

    @abstractmethod
    def _get_blame(self, commit_hash: str, path: str, hashes_to_ignore_path: str = None):
        pass

    @staticmethod
    def _useless_line(line: str):
        # this covers comments in Java and Python, as well as empty lines.
        # More have to be added!
        return not line or \
               line.startswith('//') or \
               line.startswith('#') or \
               line.startswith("/*") or \
               line.startswith("'''") or \
               line.startswith('"""') or \
               line.startswith("*")

    @abstractmethod
    def get_commits_modified_file(self, filepath: str) -> List[str]:
        pass
