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
from typing import List, Dict, Tuple, Set, Generator

# from git import Git, Repo, GitCommandError, Commit as GitCommit
import pygit2
from pygit2 import Commit as PyCommit, Repository as PyRepo, \
    GIT_CHECKOUT_FORCE, GIT_SORT_NONE, GIT_CHECKOUT_RECREATE_MISSING
from pygit2 import GIT_SORT_REVERSE

import subprocess

from pydriller.domain.commit import Commit, ModificationType, Modification

logger = logging.getLogger(__name__)

NULL_TREE = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'


class GitRepositoryException(Exception):
    pass


class GitRepository:
    """
    Class representing a repository in Git. It contains most of the logic of
    PyDriller: obtaining the list of commits, checkout, reset, etc.
    """

    def __init__(self, path: str):
        """
        Init the Git RepositoryMining.

        :param str path: path to the repository
        """
        self.path = Path(path)
        self.project_name = self.path.name
        self.main_branch = None
        self._hyper_blame_available = None
        self._repo = None

    @property
    def repo(self) -> PyRepo:
        """
        GitPython object Repo.

        :return: Repo
        """
        if self._repo is None:
            self._open_repository()
        return self._repo

    @property
    def hyper_blame_available(self):
        # Try running 'git hyper-blame' on a file in the repo to check if
        # the command is available.
        if self._hyper_blame_available is None:
            try:
                self.execute(["git", "hyper-blame", "-h"])
                self._hyper_blame_available = True
            except GitRepositoryException:
                logger.debug("Hyper-blame not available. Using normal blame.")
                self._hyper_blame_available = False
        return self._hyper_blame_available

    def _open_repository(self):
        self._repo = PyRepo(str(self.path))
        if self.main_branch is None:
            self._discover_main_branch(self._repo)

    def _discover_main_branch(self, repo):
        if not repo.head_is_detached:
            print("main branch is " + repo.head.shorthand)
            self.main_branch = repo.head.shorthand
        else:
            print("No main branch since the head is detached")
            self.main_branch = ''

    def get_head(self) -> Commit:
        """
        Get the head commit.

        :return: Commit of the head commit
        """
        head_commit = self.repo[self.repo.head.target]
        return Commit(head_commit, self.path, self.main_branch)

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
        return Commit(self.repo[commit_id], self.path, self.main_branch)

    def get_commit_from_pygit2(self, commit: PyCommit) -> Commit:
        """
        Build a PyDriller commit object from a GitPython commit object.
        This is internal of PyDriller, I don't think users generally will need
        it.

        :param GitCommit commit: GitPython commit
        :return: Commit commit: PyDriller commit
        """
        return Commit(commit, self.path, self.main_branch)

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
            return Commit(self.repo.lookup_reference("refs/tags/" + tag).peel(),
                          self.path,
                          self.main_branch)
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

    def parse_diff(self, diff: str) -> Dict[str, List[Tuple[int, str]]]:
        """
        Given a diff, returns a dictionary with the added and deleted lines.
        The dictionary has 2 keys: "added" and "deleted", each containing the
        corresponding added or deleted lines. For both keys, the value is a
        list of Tuple (int, str), corresponding to (number of line in the file,
        actual line).


        :param str diff: diff of the commit
        :return: Dictionary
        """
        lines = diff.split('\n')
        modified_lines = {'added': [], 'deleted': []}

        count_deletions = 0
        count_additions = 0

        for line in lines:
            line = line.rstrip()
            count_deletions += 1
            count_additions += 1

            if line.startswith('@@'):
                count_deletions, count_additions = self._get_line_numbers(line)

            if line.startswith('-') and not line.startswith('---'):
                modified_lines['deleted'].append((count_deletions, line[1:]))
                count_additions -= 1

            if line.startswith('+') and not line.startswith('+++'):
                modified_lines['added'].append((count_additions, line[1:]))
                count_deletions -= 1

            if line == r'\ No newline at end of file':
                count_deletions -= 1
                count_additions -= 1

        return modified_lines

    def execute(self, command: List[str], cwd: str = None) -> str:
        if not cwd:
            cwd = str(self.path)
        try:
            return subprocess.check_output(command, cwd=cwd,
                                           stderr=subprocess.STDOUT,
                                           universal_newlines=True).strip()
        except subprocess.CalledProcessError as e:
            raise GitRepositoryException('GitReposiory.execute() failed. '
                                         'Check the message above!') from e

    def _get_line_numbers(self, line):
        token = line.split(" ")
        numbers_old_file = token[1]
        numbers_new_file = token[2]
        delete_line_number = int(numbers_old_file.split(",")[0]
                                 .replace("-", "")) - 1
        additions_line_number = int(numbers_new_file.split(",")[0]) - 1
        return delete_line_number, additions_line_number

    def get_commits_last_modified_lines(self, commit: Commit,
                                        modification: Modification = None,
                                        hashes_to_ignore_path: str = None) \
            -> Dict[str, Set[str]]:
        """
        Given the Commit object, returns the set of commits that last
        "touched" the lines that are modified in the files included in the
        commit. It applies SZZ.

        IMPORTANT: for better results, we suggest to install Google
        depot_tools first (see
        https://dev.chromium.org/developers/how-tos/install-depot-tools).
        This allows PyDriller to use "git hyper-blame" instead of the normal
        blame. If depot_tools are not installed, PyDriller will automatically
        switch to the normal blame.

        The algorithm works as follow: (for every file in the commit)

        1- obtain the diff

        2- obtain the list of deleted lines

        3- blame the file and obtain the commits were those lines were added

        Can also be passed as parameter a single Modification, in this case
        only this file will be analyzed.

        :param Commit commit: the commit to analyze
        :param Modification modification: single modification to analyze
        :param str hashes_to_ignore_path: path to a file containing hashes of
               commits to ignore. Requires "git hyper-blame".
        :return: the set containing all the bug inducing commits
        """
        if hashes_to_ignore_path is not None:
            assert self.hyper_blame_available, "Can't ignore hashes if " \
                                               "hyper-blame is not " \
                                               "available. Install it by " \
                                               "cloning depot_tools and " \
                                               "adding it to your PATH."
            hashes_to_ignore_path = os.path.realpath(hashes_to_ignore_path)
            assert os.path.exists(hashes_to_ignore_path), "The file with the commit hashes to ignore does not exist"

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

        buggy_commits = {}

        for mod in modifications:
            path = mod.new_path
            if mod.change_type == ModificationType.RENAME or \
                    mod.change_type == ModificationType.DELETE:
                path = mod.old_path
            deleted_lines = self.parse_diff(mod.diff)['deleted']
            try:
                blame = self._get_blame(commit.hash, path,
                                        hashes_to_ignore_path)
                for num_line, line in deleted_lines:
                    print(line.strip())
                    if not self._useless_line(line.strip()):
                        buggy_commit = blame[num_line - 1].split(' ')[
                            0].replace('^', '')

                        if mod.change_type == ModificationType.RENAME:
                            path = mod.new_path

                        buggy_commits.setdefault(path, set()).add(
                            self.get_commit(buggy_commit).hash)
            except GitRepositoryException:
                logger.debug(
                    "Could not found file %s in commit %s. Probably a double "
                    "rename!", mod.filename, commit.hash)

        return buggy_commits

    def _get_blame(self, hash: str, path: str,
                   hashes_to_ignore_path: str = None):
        """
        If "git hyper-blame" is available, use it. Otherwise use normal blame.
        """
        if not self.hyper_blame_available or hashes_to_ignore_path is None:
            cmd = ["git", "blame", "-w", hash + '^', "--", path]
            return self.execute(cmd).split('\n')
        else:
            cmd = ["git", "hyper-blame", hash + '^', path]
            if hashes_to_ignore_path is not None:
                cmd.append("--ignore-file={}"
                           .format(hashes_to_ignore_path))
            return self.execute(cmd).split('\n')

    def _useless_line(self, line: str):
        # this covers comments in Java and Python, as well as empty lines.
        # More have to be added!
        return not line or \
               line.startswith('//') or \
               line.startswith('#') or \
               line.startswith("/*") or \
               line.startswith("'''") or \
               line.startswith('"""') or \
               line.startswith("*")

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
