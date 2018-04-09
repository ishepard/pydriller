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

import os
import logging
from typing import List, Dict, Tuple
from git import Git, Repo, Diff, GitCommandError
from pydriller.domain.commit import Commit, ChangeSet
from pydriller.domain.developer import Developer
from pydriller.domain.modification import ModificationType
from threading import Lock

logger = logging.getLogger(__name__)


class GitRepository:
    def __init__(self, path: str):
        """
        Init the Git Repository.

        :param path: path to the repository
        """
        self.path = path
        self.main_branch = None
        self.lock = Lock()

    def _open_git(self) -> Git:
        self._open_repository()
        return Git(self.path)

    def _open_repository(self) -> Repo:
        repo = Repo(self.path)
        if self.main_branch is None:
            self._discover_main_branch(repo)
        return repo

    def _discover_main_branch(self, repo):
        self.main_branch = repo.active_branch.name

    def get_head(self) -> ChangeSet:
        """
        Get the head commit.

        :return: ChangeSet of the head commit
        """
        repo = self._open_repository()
        head_commit = repo.head.commit
        return ChangeSet(head_commit.hexsha, head_commit.committed_datetime)

    def get_change_sets(self) -> List[ChangeSet]:
        """
        Return the list of all the commits in the repo.

        :return: List[ChangeSet], the list of all the commits in the repo
        """
        return self._get_all_commits()

    def _get_all_commits(self) -> List[ChangeSet]:
        repo = self._open_repository()
        commit_list = list(repo.iter_commits())

        change_sets = []
        for commit in commit_list:
            committer_date = commit.committed_datetime
            change_sets.append(ChangeSet(commit.hexsha, committer_date))
        return change_sets

    def get_commit(self, commit_id: str) -> Commit:
        """
        Get the specified commit.

        :param commit_id: hash of the commit to analyze
        :return: Commit
        """
        git = self._open_git()
        repo = self._open_repository()
        commit = repo.commit(commit_id)

        author = Developer(commit.author.name, commit.author.email)
        committer = Developer(commit.committer.name, commit.committer.email)
        author_timezone = commit.author_tz_offset
        committer_timezone = commit.committer_tz_offset

        msg = commit.message.strip()
        commit_hash = commit.hexsha

        author_date = commit.authored_datetime
        committer_date = commit.committed_datetime

        merge = True if len(commit.parents) > 1 else False

        parents = []
        for p in commit.parents:
            parents.append(p.hexsha)

        branches = self._get_branches(git, commit_hash)
        is_in_main_branch = self.main_branch in branches

        the_commit = Commit(commit_hash, author, committer, author_date, committer_date, author_timezone,
                            committer_timezone, msg,
                            parents, merge, branches, is_in_main_branch)

        if len(parents) > 0:
            parent = repo.commit(parents[0])
            diff_index = parent.diff(commit, create_patch=True)
        else:
            parent = repo.tree('4b825dc642cb6eb9a060e54bf8d69288fbee4904')
            diff_index = parent.diff(commit.tree, create_patch=True)

        self._parse_diff(diff_index, the_commit)

        return the_commit

    def _parse_diff(self, diff_index, the_commit) -> None:
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
                logger.debug('Could not load source code or the diff of a file in commit {}'.format(the_commit.hash))

            the_commit.add_modifications(old_path, new_path, change_type, diff_text, sc)

    def _get_branches(self, git: Git, commit_hash: str) -> set():
        branches = set()
        for branch in set(git.branch('--contains', commit_hash).split('\n')):
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

    def checkout(self, _hash: str) -> None:
        """
        Checkout the repo at the speficied commit.
        BE CAREFUL: this will change the state of the repo, hence it should *not*
        be used with more than 1 thread.

        :param _hash: commit hash to checkout
        """
        with self.lock:
            git = self._open_git()
            self._delete_tmp_branch()
            git.checkout('-f', _hash, b='_PD')

    def _delete_tmp_branch(self) -> None:
        repo = self._open_repository()
        try:
            repo.delete_head('_PD')
        except GitCommandError:
            logger.debug("Branch _PD not found")

    def files(self) -> List[str]:
        """
        Obtain the list of the files (excluding .git directory).

        :return: List[str], the list of the files
        """
        _all = []
        for path, subdirs, files in os.walk(self.path):
            if '.git' in path:
                continue
            for name in files:
                _all.append(os.path.join(path, name))
        return _all

    def reset(self) -> None:
        """
        Reset the state of the repo, checking out the main branch and discarding
        local changes (-f option).

        """
        with self.lock:
            git = self._open_git()
            git.checkout('-f', self.main_branch)
            self._delete_tmp_branch()

    def total_commits(self) -> int:
        """
        Calculate total number of commits.

        :return: the total number of commits
        """
        return len(self.get_change_sets())

    def get_commit_from_tag(self, tag: str) -> Commit:
        """
        Obtain the tagged commit.

        :param str tag: the tag
        :return: Commit commit: the commit the tag referred to
        """
        repo = self._open_repository()
        try:
            selected_tag = repo.tags[tag]
            return self.get_commit(selected_tag.commit.hexsha)
        except (IndexError, AttributeError):
            logger.debug('Tag {} not found'.format(tag))
            raise

    def parse_diff(self, diff: str) -> Dict[str, List[Tuple[int, str]]]:
        """
        Given a diff, returns a dictionary with the added and deleted lines.
        The dictionary has 2 keys: "added" and "deleted", each containing the
        corresponding added or deleted lines. For both keys, the value is a list
        of Tuple (int, str), corresponding to (number of line in the file, actual line).


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

            if line.startswith('-'):
                modified_lines['deleted'].append((count_deletions, line[1:]))
                count_additions -= 1

            if line.startswith('+'):
                modified_lines['added'].append((count_additions, line[1:]))
                count_deletions -= 1

        return modified_lines

    def _get_line_numbers(self, line):
        token = line.split(" ")
        numbers_old_file = token[1]
        numbers_new_file = token[2]
        delete_line_number = int(numbers_old_file.split(",")[0].replace("-", "")) - 1
        additions_line_number = int(numbers_new_file.split(",")[0]) - 1
        return delete_line_number, additions_line_number
