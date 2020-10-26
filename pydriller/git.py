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
import re
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Set, Generator

from git import Git as GGitPython, Repo, GitCommandError, Commit as GitCommit

from pygit2 import Commit as PyCommit, Repository as PyRepo, \
    GIT_CHECKOUT_FORCE, GIT_SORT_NONE, GIT_CHECKOUT_RECREATE_MISSING, \
    GIT_SORT_REVERSE

from pydriller.domain.commit import Commit, CommitGP, CommitPG2, ModificationType, Modification
from pydriller.utils.common import get_files
from pydriller.utils.conf import Conf

logger = logging.getLogger(__name__)


class Git(ABC):
    """
    Class representing a repository in Git. It contains most of the logic of
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
        """
        Get the head commit.

        :return: Commit of the head commit
        """
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
    def total_commits(self) -> int:
        pass

    @abstractmethod
    def get_commit_from_tag(self, tag: str) -> Commit:
        pass

    @abstractmethod
    def get_blame(self, commit_hash: str, path: str, hashes_to_ignore_path: str = None):
        pass

    @abstractmethod
    def get_tagged_commits(self):
        pass

    @abstractmethod
    def get_commits_modified_file(self, filepath: str) -> List[str]:
        pass

    def files(self) -> List[str]:
        """
        Obtain the list of the files (excluding .git directory).

        :return: List[str], the list of the files
        """
        return get_files(str(self.path))

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
                blame = self.get_blame(commit.hash, path, hashes_to_ignore_path)
                for num_line, line in deleted_lines:
                    if not self._useless_line(line.strip()):
                        buggy_commit = blame[num_line - 1].split(' ')[0].replace('^', '')

                        # Skip unblamable lines.
                        if buggy_commit.startswith("*"):
                            continue

                        if mod.change_type == ModificationType.RENAME:
                            path = mod.new_path

                        commits.setdefault(path, set()).add(self.get_commit(buggy_commit).hash)
            except (GitCommandError, subprocess.CalledProcessError) as e:
                logger.debug(
                    "Could not found file %s in commit %s. Probably a double "
                    "rename!", mod.filename, commit.hash)

        return commits

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


class GitGP(Git):
    """
    Class representing a repository in GitGP. It contains most of the logic of
    PyDriller: obtaining the list of commits, checkout, reset, etc.
    """

    def __init__(self, path: str, conf=None):
        """
        Init the GitGP Repository.

        :param str path: path to the repository
        """
        super().__init__(path, conf)

    @property
    def git(self):
        """
        GitGP object GitGP.

        :return: GitGP
        """
        if self._git is None:
            self._open_git()
        return self._git

    @property
    def repo(self):
        """
        GitGP object Repo.

        :return: Repo
        """
        if self._repo is None:
            self._open_repository()
        return self._repo

    def _open_git(self):
        self._git = GGitPython(str(self.path))

    def clear(self):
        """
        According to GitGP's documentation, sometimes it leaks resources.
        This holds especially for Windows users. Hence, we need to clear the
        cache manually.
        """
        if self._git:
            self.git.clear_cache()
        if self._repo:
            self.repo.git.clear_cache()

    def _open_repository(self):
        self._repo = Repo(str(self.path))
        self._repo.config_writer().set_value("blame", "markUnblamableLines", "true").release()
        if self._conf.get("main_branch") is None:
            self._discover_main_branch(self._repo)

    def _discover_main_branch(self, repo):
        try:
            self._conf.set_value("main_branch", repo.active_branch.name)
        except TypeError:
            # The current HEAD is detached. In this case, it doesn't belong to
            # any branch, hence we return an empty string
            logger.info("HEAD is a detached symbolic reference, setting main branch to empty string")
            self._conf.set_value("main_branch", '')

    def get_head(self) -> Commit:
        head_commit = self.repo.head.commit
        return CommitGP(head_commit, self._conf)

    def get_list_commits(self, rev='HEAD', **kwargs) -> Generator[Commit, None, None]:
        """
        Return a generator of commits of all the commits in the repo.

        :return: Generator[Commit], the generator of all the commits in the
            repo
        """
        # If not specified otherwise, analyze the repository in reversed order
        if 'reverse' not in kwargs:
            kwargs['reverse'] = True

        for commit in self.repo.iter_commits(rev=rev, **kwargs):
            yield self.get_commit_from_gitpython(commit)

    def get_commit(self, commit_id: str) -> Commit:
        """
        Get the specified commit.

        :param str commit_id: hash of the commit to analyze
        :return: Commit
        """
        return CommitGP(self.repo.commit(commit_id), self._conf)

    def get_commit_from_gitpython(self, commit: GitCommit) -> Commit:
        """
        Build a PyDriller commit object from a GitGP commit object.
        This is internal of PyDriller, I don't think users generally will need
        it.

        :param GitCommit commit: GitGP commit
        :return: Commit commit: PyDriller commit
        """
        return CommitGP(commit, self._conf)

    def checkout(self, _hash: str) -> None:
        """
        Checkout the repo at the speficied commit.
        BE CAREFUL: this will change the state of the repo, hence it should
        *not* be used with more than 1 thread.

        :param _hash: commit hash to checkout
        """
        self.git.checkout('-f', _hash)

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
            selected_tag = self.repo.tags[tag]
            return self.get_commit(selected_tag.commit.hexsha)
        except (IndexError, AttributeError):
            logger.debug('Tag %s not found', tag)
            raise

    def get_tagged_commits(self):
        """
        Obtain the hash of all the tagged commits.

        :return: list of tagged commits (can be empty if there are no tags)
        """
        tags = []
        for tag in self.repo.tags:
            if tag.commit:
                tags.append(tag.commit.hexsha)
        return tags

    def get_blame(self, commit_hash: str, path: str, hashes_to_ignore_path: str = None):
        args = ['-w', commit_hash + '^']
        if hashes_to_ignore_path is not None:
            if self.git.version_info >= (2, 23):
                args += ["--ignore-revs-file", hashes_to_ignore_path]
            else:
                logger.info("'--ignore-revs-file' is only available from git v2.23")
        return self.git.blame(*args, '--', path).split('\n')

    def get_commits_modified_file(self, filepath: str) -> List[str]:
        """
        Given a filepath, returns all the commits that modified this file
        (following renames).

        :param str filepath: path to the file
        :return: the list of commits' hash
        """
        path = str(Path(filepath))

        commits = []
        try:
            commits = self.git.log("--follow", "--format=%H", path).split('\n')
        except GitCommandError:
            logger.debug("Could not find information of file %s", path)

        return commits

    def __del__(self):
        self.clear()


class GitPG2(Git):
    """
    Class representing a repository in Git. It contains most of the logic of
    PyDriller: obtaining the list of commits, checkout, reset, etc.
    """
    def __init__(self, path: str, conf=None):
        """
        Init the Git RepositoryMining.

        :param str path: path to the repository
        """
        super().__init__(path, conf)

    @property
    def repo(self) -> PyRepo:
        """
        GitPG2 object Repo.

        :return: Repo
        """
        if self._repo is None:
            self._open_repository()
        return self._repo

    def _open_repository(self):
        self._repo = PyRepo(str(self.path))
        if self._conf.get("main_branch") is None:
            self._discover_main_branch(self._repo)

    def _discover_main_branch(self, repo):
        if not repo.head_is_detached:
            self._conf.set_value("main_branch", repo.head.shorthand)
        else:
            self._conf.set_value("main_branch", '')

    def get_head(self) -> Commit:
        """
        Get the head commit.

        :return: Commit of the head commit
        """
        head_commit = self.repo[self.repo.head.target]
        return CommitPG2(head_commit, self._conf)

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
        return CommitPG2(self.repo[commit_id], self._conf)

    def get_commit_from_pygit2(self, commit: PyCommit) -> Commit:
        """
        Build a PyDriller commit object from a pygit2 commit object.
        This is internal of PyDriller, I don't think users generally will need
        it.

        :param pygit2 commit: pygit2 commit
        :return: Commit commit: PyDriller commit
        """
        return CommitPG2(commit, self._conf)

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
            return CommitPG2(self.repo.lookup_reference("refs/tags/" + tag).peel(), self._conf)
        except KeyError:
            logger.debug('Tag %s not found', tag)
            raise IndexError

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

    def get_blame(self, commit_hash: str, path: str, hashes_to_ignore_path: str = None):
        cmd = ["git", "blame", "-w", commit_hash + '^']
        if hashes_to_ignore_path is not None:
            cmd += ["--ignore-revs-file", hashes_to_ignore_path]
        cmd += ["--", path]
        return self._execute(cmd).split('\n')

    def _execute(self, command: List[str], cwd: str = None) -> str:
        if not cwd:
            cwd = str(self.path)
        try:
            return subprocess.check_output(command, cwd=cwd,
                                           stderr=subprocess.STDOUT,
                                           universal_newlines=True).strip()
        except subprocess.CalledProcessError as e:
            logger.info('GitReposiory.execute() failed. Check the message above!')
            print(e)
            raise

    def get_commits_modified_file(self, filepath: str) -> List[str]:
        """
        Given a filepath, returns all the commits that modified this file
        (following renames).

        :param str filepath: path to the file
        :return: the list of commits' hash
        """
        path = str(Path(filepath))

        cmd = ["git", "log", "--follow", "--format=%H", path]
        commits = []
        try:
            commits = self._execute(cmd).split('\n')
        except subprocess.CalledProcessError:
            logger.debug("Could not find information of file %s", path)

        return commits
