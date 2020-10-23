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
This module includes 1 class, GitRepository, representing a repository in Git.
"""

import logging
import os
import re
from pathlib import Path
from typing import List, Generator

from pygit2 import Commit as PyCommit, Repository as PyRepo, \
    GIT_CHECKOUT_FORCE, GIT_SORT_NONE, GIT_CHECKOUT_RECREATE_MISSING, \
    GIT_SORT_REVERSE

import subprocess

from pydriller.domain.commit import Commit
from pydriller.git import Git
from pydriller.utils.conf import Conf

logger = logging.getLogger(__name__)

NULL_TREE = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'


class Pygit2(Git):
    """
    Class representing a repository in Git. It contains most of the logic of
    PyDriller: obtaining the list of commits, checkout, reset, etc.
    """
    def __init__(self, path: str, conf: Conf):
        """
        Init the Git RepositoryMining.

        :param str path: path to the repository
        """
        super().__init__(path, conf)

    @property
    def repo(self) -> PyRepo:
        """
        Pygit2 object Repo.

        :return: Repo
        """
        if self._repo is None:
            self._open_repository()
        return self._repo

    def _open_repository(self):
        self._repo = PyRepo(str(self.path))
        if self.main_branch is None:
            self._discover_main_branch(self._repo)

    def _discover_main_branch(self, repo):
        if not repo.head_is_detached:
            self.main_branch = repo.head.shorthand
        else:
            self.main_branch = ''

    def get_head(self) -> Commit:
        """
        Get the head commit.

        :return: Commit of the head commit
        """
        head_commit = self.repo[self.repo.head.target]
        return Commit(head_commit, self._conf)

    def get_list_commits(self, branch: str = None,
                         reverse_order: bool = True) \
            -> Generator[Commit, None, None]:
        """
        Return a generator of commits of all the commits in the repo.

        :return: Generator[Commit], the generator of all the commits in the
            repo
        """
        sort = GIT_SORT_REVERSE
        if not reverse_order:
            sort = GIT_SORT_NONE

        if branch:
            target = self.repo.branches[branch].target
        else:
            target = self.repo.head.target

        for commit in self.repo.walk(target, sort):
            yield self.get_commit_from_pygit2(commit)

    def get_commit(self, commit_id: str) -> Commit:
        """
        Get the specified commit.

        :param str commit_id: hash of the commit to analyze
        :return: Commit
        """
        return Commit(self.repo[commit_id], self._conf)

    def get_commit_from_pygit2(self, commit: PyCommit) -> Commit:
        """
        Build a PyDriller commit object from a pygit2 commit object.
        This is internal of PyDriller, I don't think users generally will need
        it.

        :param pygit2 commit: pygit2 commit
        :return: Commit commit: PyDriller commit
        """
        return Commit(commit, self._conf)

    def checkout(self, ref: str) -> None:
        """
        Checkout the repo at the speficied commit.
        BE CAREFUL: this will change the state of the repo, hence it should
        *not* be used with more than 1 thread.

        :param ref: commit hash or branch name to checkout
        """
        try:
            # first check if it's a branch
            self.repo.lookup_reference('refs/heads/' + ref)
            branch = True
        except KeyError:
            # ref is a commit
            branch = False
        if branch:
            self.repo.checkout('refs/heads/' + ref,
                               strategy=GIT_CHECKOUT_FORCE |
                               GIT_CHECKOUT_RECREATE_MISSING)
        else:
            self.repo.checkout_tree(self.repo[ref],
                                    strategy=GIT_CHECKOUT_FORCE |
                                    GIT_CHECKOUT_RECREATE_MISSING)
            self.repo.set_head(self.repo[ref].oid)

    def files(self) -> List[str]:
        """
        Obtain the list of the files (excluding .git directory).

        :return: List[str], the list of the files
        """
        _all = []
        for path, _, files in os.walk(str(self.path)):
            if '.git' in path:
                continue
            for name in files:
                _all.append(os.path.join(path, name))
        return _all

    def total_commits(self) -> int:
        """
        Calculate total number of commits.

        :return: the total number of commits
        """
        return len(list(self.get_list_commits()))

    def get_commit_from_tag(self, tag: str) -> Commit:
        """
        Obtain the tagged commit.

        :param str tag: the tag
        :return: Commit commit: the commit the tag referred to
        """
        try:
            return Commit(self.repo.lookup_reference("refs/tags/" + tag).peel(), self._conf)
        except KeyError:
            logger.debug('Tag %s not found', tag)
            raise

    def get_tagged_commits(self):
        """
        Obtain the hash of all the tagged commits.

        :return: list of tagged commits (can be empty if there are no tags)
        """
        tags = []
        regex = re.compile('^refs/tags')
        for tag in filter(lambda r: regex.match(r), self.repo.references):
            tag_ref = self.repo.lookup_reference(tag)
            tags.append(tag_ref.peel().hex)
        return tags

    def _get_blame(self, commit_hash: str, path: str, hashes_to_ignore_path: str = None):
        cmd = ["git", "blame", "-w", commit_hash + '^', "--", path]
        if hashes_to_ignore_path is not None:
            cmd += ["--ignore-revs-file", hashes_to_ignore_path]
        return self.execute(cmd).split('\n')

    def execute(self, command: List[str], cwd: str = None) -> str:
        if not cwd:
            cwd = str(self.path)
        try:
            return subprocess.check_output(command, cwd=cwd,
                                           stderr=subprocess.STDOUT,
                                           universal_newlines=True).strip()
        except subprocess.CalledProcessError as e:
            raise Exception('GitReposiory.execute() failed. Check the message above!') from e

    def get_commits_modified_file(self, filepath: str) -> List[str]:
        """
        Given a filepath, returns all the commits that modified this file
        (following renames).

        :param str filepath: path to the file
        :return: the list of commits' hash
        """
        path = str(Path(filepath))

        cmd = ["git", "log", "--follow", "--format=%H", path]
        return self.execute(cmd).split('\n')