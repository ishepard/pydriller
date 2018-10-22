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

import atexit
import logging
import os
import shutil
import tempfile
from datetime import datetime
from typing import List, Generator, Union

import pytz as pytz
from git import Repo, GitCommandError

from pydriller.domain.commit import Commit
from pydriller.git_repository import GitRepository

logger = logging.getLogger(__name__)


class RepositoryMining:
    def __init__(self, path_to_repo: Union[str, List[str]],
                 single: str = None,
                 since: datetime = None, to: datetime = None,
                 from_commit: str = None, to_commit: str = None,
                 from_tag: str = None, to_tag: str = None,
                 reversed_order: bool = False,
                 only_in_main_branch: bool = False,
                 only_in_branches: List[str] = None,
                 only_modifications_with_file_types: List[str] = None,
                 only_no_merge: bool = False):
        """
        Init a repository mining.

        :param str or List[str] path_to_repo: absolute path to the repository (or list of absolute paths) you have to analyze
        :param str single: hash of a single commit to analyze
        :param datetime since: starting date
        :param datetime to: ending date
        :param str from_commit: starting commit (only if `since` is None)
        :param str to_commit: ending commit (only if `to` is None)
        :param str from_tag: starting the analysis from specified tag (only if `since` and `from_commit` are None)
        :param str to_tag: ending the analysis from specified tag (only if `to` and `to_commit` are None)
        :param bool reversed_order: whether the commits should be analyzed in reversed order
        :param bool only_in_main_branch: whether only commits in main branch should be analyzed
        :param List[str] only_in_branches: only commits in these branches will be analyzed
        :param List[str] only_modifications_with_file_types: only modifications with that file types will be analyzed
        :param bool only_no_merge: if True, merges will not be analyzed
        """

        self._sanity_check_repos(path_to_repo)
        self._path_to_repo = path_to_repo

        self.from_commit = from_commit
        self.to_commit = to_commit
        self.from_tag = from_tag
        self.to_tag = to_tag
        self.single = single
        self.since = since
        self.to = to
        self.reversed_order = reversed_order
        self.only_in_main_branch = only_in_main_branch
        self.only_in_branches = only_in_branches
        self.only_modifications_with_file_types = only_modifications_with_file_types
        self.only_no_merge = only_no_merge

    def _sanity_check_repos(self, path_to_repo):
        if not isinstance(path_to_repo, str) and not isinstance(path_to_repo, list):
            raise Exception('The path to the repo has to be of type \"string\" or \"list of strings\"!')

    def _sanity_check_filters(self, git_repo, from_commit, from_tag, since, single, to, to_commit, to_tag):
        if single is not None:
            if since is not None or to is not None or from_commit is not None or \
                    to_commit is not None or from_tag is not None or to_tag is not None:
                raise Exception('You can not specify a single commit with other filters')

        if from_commit is not None:
            if since is not None:
                raise Exception('You can not specify both <since date> and <from commit>')
            self.since = git_repo.get_commit(from_commit).author_date

        if to_commit is not None:
            if to is not None:
                raise Exception('You can not specify both <to date> and <to commit>')
            self.to = git_repo.get_commit(to_commit).author_date

        if from_tag is not None:
            if since is not None or from_commit is not None:
                raise Exception('You can not specify <since date> or <from commit> when using <from tag>')
            self.since = git_repo.get_commit_from_tag(from_tag).author_date

        if to_tag is not None:
            if to is not None or to_commit is not None:
                raise Exception('You can not specify <to date> or <to commit> when using <to tag>')
            self.to = git_repo.get_commit_from_tag(to_tag).author_date

    def isremote(self, repo: str) -> bool:
        return repo.startswith("git@") or repo.startswith("https://")

    def clone_remote_repos(self, tmp_folder: str, repo: str) -> str:

        repo_folder = os.path.join(tmp_folder, self.get_repo_name_from_url(repo))
        logger.info("Cloning {} in temporary folder {}".format(repo, repo_folder))
        try:
            Repo.clone_from(url=repo, to_path=repo_folder)
        except GitCommandError:
            raise Exception("Could not clone {} in temporary folder {} since the folder "
                            "already exists or it is not an empty directory".format(repo, repo_folder))

        return repo_folder

    def traverse_commits(self) -> Generator[Commit, None, None]:
        """
        Analyze all the specified commits (all of them by default), returning
        a generator of commits.
        """

        if isinstance(self._path_to_repo, str):
            self._path_to_repo = [self._path_to_repo]

        for path_repo in self._path_to_repo:
            # if it is a remote repo, clone it first in a temporary folder!
            if self.isremote(path_repo):
                tmp_folder = tempfile.TemporaryDirectory()
                path_repo = self.clone_remote_repos(tmp_folder.name, path_repo)

            git_repo = GitRepository(path_repo)

            self._sanity_check_filters(git_repo, self.from_commit, self.from_tag, self.since,
                                       self.single, self.to, self.to_commit, self.to_tag)
            self._check_timezones()

            logger.info('Analyzing git repository in {}'.format(git_repo.path))
            all_cs = self._apply_filters_on_commits(git_repo.get_list_commits())

            if not self.reversed_order:
                all_cs.reverse()

            for commit in all_cs:
                logger.info('Commit #{} in {} from {}'
                            .format(commit.hash, commit.author_date, commit.author.name))

                if self._is_commit_filtered(commit):
                    logger.info('Commit #{} filtered'.format(commit.hash))
                    continue

                yield commit

    def _is_commit_filtered(self, commit: Commit):
        if self.only_in_main_branch is True and commit.in_main_branch is False:
            logger.debug('Commit filtered for main branch')
            return True
        if self.only_in_branches is not None:
            logger.debug('Commit filtered for only in branches')
            if not self._commit_branch_in_branches(commit):
                return True
        if self.only_modifications_with_file_types is not None:
            logger.debug('Commit filtered for modification types')
            if not self._has_modification_with_file_type(commit):
                return True
        if self.only_no_merge is True and commit.merge is True:
            logger.debug('Commit filtered for no merge')
            return True
        return False

    def _commit_branch_in_branches(self, commit: Commit):
        for branch in commit.branches:
            if branch in self.only_in_branches:
                return True
        return False

    def _has_modification_with_file_type(self, commit):
        for mod in commit.modifications:
            if mod.filename.endswith(tuple(self.only_modifications_with_file_types)):
                return True
        return False

    def _apply_filters_on_commits(self, all_commits: List[Commit]):
        res = []

        if self._all_filters_are_none():
            return all_commits

        for commit in all_commits:
            if self.single is not None and commit.hash == self.single:
                return [commit]
            if self.since is None or self.since <= commit.author_date:
                if self.to is None or commit.author_date <= self.to:
                    res.append(commit)
                    continue
        return res

    def _all_filters_are_none(self):
        return self.single is None and self.since is None and self.to is None

    def _check_timezones(self):
        if self.since is not None:
            if self.since.tzinfo is None or self.since.tzinfo.utcoffset(self.since) is None:
                self.since = self.since.replace(tzinfo=pytz.utc)
        if self.to is not None:
            if self.to.tzinfo is None or self.to.tzinfo.utcoffset(self.to) is None:
                self.to = self.to.replace(tzinfo=pytz.utc)

    def get_repo_name_from_url(self, url: str) -> str:
        last_slash_index = url.rfind("/")
        last_suffix_index = url.rfind(".git")
        if last_suffix_index < 0:
            last_suffix_index = len(url)

        if last_slash_index < 0 or last_suffix_index <= last_slash_index:
            raise Exception("Badly formatted url {}".format(url))

        return url[last_slash_index + 1:last_suffix_index]
