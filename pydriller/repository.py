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
This module includes 1 class, Repository, main class of PyDriller.
"""

import logging
import math
import os
import shutil
import tempfile
import concurrent.futures
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import List, Generator, Optional, Union

from git import Repo

from pydriller.domain.commit import Commit
from pydriller.git import Git
from pydriller.utils.conf import Conf

logger = logging.getLogger(__name__)


class Repository:
    """
    This is the main class of PyDriller, responsible for running the study.
    """

    def __init__(self, path_to_repo: Union[str, os.PathLike, List[str], List[os.PathLike]],
                 single: Optional[str] = None,
                 since: Optional[datetime] = None, since_as_filter: Optional[datetime] = None, to: Optional[datetime] = None,
                 from_commit: Optional[str] = None, to_commit: Optional[str] = None,
                 from_tag: Optional[str] = None, to_tag: Optional[str] = None,
                 include_refs: bool = False,
                 include_remotes: bool = False,
                 num_workers: int = 1,
                 only_in_branch: Optional[str] = None,
                 only_modifications_with_file_types: Optional[List[str]] = None,
                 only_no_merge: bool = False,
                 only_authors: Optional[List[str]] = None,
                 only_commits: Optional[List[str]] = None,
                 only_releases: bool = False,
                 filepath: Optional[str] = None,
                 include_deleted_files: bool = False,
                 histogram_diff: bool = False,
                 skip_whitespaces: bool = False,
                 clone_repo_to: Optional[Union[str, os.PathLike]] = None,
                 order: Optional[str] = None,
                 use_mailmap: bool = False):
        """
        Init a repository. The only required parameter is
        "path_to_repo": to analyze a single repo, pass the absolute path to
        the repo; if you need to analyze more repos, pass a list of absolute
        paths.

        Furthermore, PyDriller supports local and remote repositories: if
        you pass a path to a repo, PyDriller will run the study on that
        repo; if you pass an URL, PyDriller will clone the repo in a
        temporary folder, run the study, and delete the temporary folder.

        :param Union[os.PathLike, List[os.PathLike] path_to_repo: PathLike object (or list of
            PathLike objects) to the repository(ies) to analyze
        :param str single: hash of a single commit to analyze
        :param datetime since: starting date
        :param datetime since_as_filter: starting date (scans all commits, does not stop at first commit with date < since_as_filter)
        :param datetime to: ending date
        :param str from_commit: starting commit (only if `since` is None)
        :param str to_commit: ending commit (only if `to` is None)
        :param str from_tag: starting the analysis from specified tag (only
            if `since` and `from_commit` are None)
        :param str to_tag: ending the analysis from specified tag (only if
            `to` and `to_commit` are None)
        :param bool include_refs: whether to include refs and HEAD in commit analysis
        :param bool include_remotes: whether to include remote commits in analysis
        :param int num_workers: number of workers (i.e., threads). Please note, if num_workers > 1 the commits order is not maintained.
        :param str only_in_branch: only commits in this branch will be analyzed
        :param List[str] only_modifications_with_file_types: only
            modifications with that file types will be analyzed
        :param bool only_no_merge: if True, merges will not be analyzed
        :param List[str] only_authors: only commits of these authors will be
            analyzed (the check is done on the username, NOT the email)
        :param List[str] only_commits: only these commits will be analyzed
        :param bool only_releases: analyze only tagged commits
        :param bool histogram_diff: add the "--histogram" option when asking for the diff
        :param bool skip_whitespaces: add the "-w" option when asking for the diff
        :param Optional[os.PathLike] clone_repo_to: if the repo under analysis is remote, clone the repo to the specified directory
        :param str filepath: only commits that modified this file will be analyzed
        :param bool include_deleted_files: include commits modifying a deleted file (useful when analyzing a deleted `filepath`)
        :param str order: order of commits. It can be one of: 'date-order',
            'author-date-order', 'topo-order', or 'reverse'. If order=None, PyDriller returns the commits from the oldest to the newest.
        :param bool use_mailmap: Map names and emails of authors and committers to canonical values when a .mailmap file is present in
            the repository.
        """
        file_modification_set = (
            None if only_modifications_with_file_types is None
            else set(only_modifications_with_file_types)
            )
        commit_set = (
            None if only_commits is None
            else set(only_commits)
            )

        try:
            if isinstance(path_to_repo, list):
                path_to_repos = [os.fspath(path) for path in path_to_repo]
            else:
                path_to_repos = [os.fspath(path_to_repo)]
        except TypeError:
            raise AttributeError("Path to repo must be PathLike or list of PathLike")

        options = {
            "git": None,
            "path_to_repo": path_to_repos,
            "from_commit": from_commit,
            "to_commit": to_commit,
            "from_tag": from_tag,
            "to_tag": to_tag,
            "since": since,
            "since_as_filter": since_as_filter,
            "to": to,
            "single": single,
            "include_refs": include_refs,
            "include_remotes": include_remotes,
            "num_workers": num_workers,
            "only_in_branch": only_in_branch,
            "only_modifications_with_file_types": file_modification_set,
            "only_no_merge": only_no_merge,
            "only_authors": only_authors,
            "only_commits": commit_set,
            "only_releases": only_releases,
            "skip_whitespaces": skip_whitespaces,
            "filepath": filepath,
            "include_deleted_files": include_deleted_files,
            "filepath_commits": None,
            "tagged_commits": None,
            "histogram": histogram_diff,
            "clone_repo_to": clone_repo_to,
            "order": order,
            "use_mailmap": use_mailmap
        }
        self._conf = Conf(options)

        # If the user provides a directory where to clone the repositories,
        # make sure we do not delete the directory after the study completes
        self._cleanup = False if clone_repo_to is not None else True

    @staticmethod
    def _is_remote(repo: os.PathLike) -> bool:
        return os.fspath(repo).startswith(("git@", "https://", "http://", "git://"))

    def _clone_remote_repo(self, tmp_folder: os.PathLike, repo: os.PathLike) -> os.PathLike:
        repo_folder = os.path.join(tmp_folder, self._get_repo_name_from_url(os.fspath(repo)))
        if os.path.isdir(repo_folder):
            logger.info(f"Reusing folder {repo_folder} for {repo}")
        else:
            logger.info(f"Cloning {repo} in temporary folder {repo_folder}")
            Repo.clone_from(url=repo, to_path=repo_folder)

        return Path(repo_folder)

    def _clone_folder(self) -> os.PathLike:
        clone_folder = self._conf.get('clone_repo_to')
        if clone_folder is not None:
            if not os.path.isdir(clone_folder):
                raise ValueError("clone_repo_to must be an existing directory")
        else:
            # Save the temporary directory so we can clean it up later
            self._tmp_dir = tempfile.TemporaryDirectory()
            clone_folder = self._tmp_dir.name
        return clone_folder

    @contextmanager
    def _prep_repo(self, path_repo: os.PathLike) -> Generator[Git, None, None]:
        local_path_repo = path_repo
        if self._is_remote(path_repo):
            local_path_repo = self._clone_remote_repo(self._clone_folder(), path_repo)
        local_path_repo = Path(local_path_repo).expanduser().resolve()

        # when multiple repos are given in input, this variable will serve as a reminder
        # of which one we are currently analyzing
        self._conf.set_value('path_to_repo', local_path_repo)

        self.git = Git(local_path_repo, self._conf)
        # saving the Git object for further use
        self._conf.set_value("git", self.git)

        # checking that the filters are set correctly
        self._conf.sanity_check_filters()
        yield self.git

        # cleaning, this is necessary since GitPython issues on memory leaks
        self._conf.set_value("git", None)
        self.git.clear()
        self.git = None  # type: ignore

        # delete the temporary directory if created
        if self._is_remote(path_repo) and self._cleanup is True:
            assert self._tmp_dir is not None
            try:
                self._tmp_dir.cleanup()
            except (PermissionError, OSError):
                # On Windows there might be cleanup errors.
                # Manually remove files
                shutil.rmtree(self._tmp_dir.name, ignore_errors=True)

    def traverse_commits(self) -> Generator[Commit, None, None]:
        """
        Analyze all the specified commits (all of them by default), returning
        a generator of commits.
        """
        for path_repo in self._conf.get('path_to_repos'):
            with self._prep_repo(path_repo=path_repo) as git:
                logger.info(f'Analyzing git repository in {git.path}')

                # Get the commits that modified the filepath. In this case, we can not use
                # git rev-list since it doesn't have the option --follow, necessary to follow
                # the renames. Hence, we manually call git log instead
                if self._conf.get('filepath') is not None:
                    self._conf.set_value(
                        'filepath_commits',
                        git.get_commits_modified_file(self._conf.get('filepath'),
                                                      self._conf.get('include_deleted_files'))
                    )

                # Gets only the commits that are tagged
                if self._conf.get('only_releases'):
                    self._conf.set_value('tagged_commits', git.get_tagged_commits())

                # Build the arguments to pass to git rev-list.
                rev, kwargs = self._conf.build_args()

                with concurrent.futures.ThreadPoolExecutor(max_workers=self._conf.get("num_workers")) as executor:
                    for job in executor.map(self._iter_commits, git.get_list_commits(rev, **kwargs)):

                        for commit in job:
                            yield commit

    def _iter_commits(self, commit: Commit) -> Generator[Commit, None, None]:
        logger.info(f'Commit #{commit.hash} in {commit.committer_date} from {commit.author.name}')

        if self._conf.is_commit_filtered(commit):
            logger.info(f'Commit #{commit.hash} filtered')
            return

        yield commit

    @staticmethod
    def _split_in_chunks(full_list: List[Commit], num_workers: int) -> List[List[Commit]]:
        """
        Given the list of commits return chunks of commits based on the number of workers.

        :param List[Commit] full_list: full list of commits
        :param int num_workers: number of workers (i.e., threads)
        :return: Chunks of commits
        """
        num_chunks = math.ceil(len(full_list) / num_workers)
        chunks = []
        for i in range(0, len(full_list), num_chunks):
            chunks.append(full_list[i:i + num_chunks])

        return chunks

    @staticmethod
    def _get_repo_name_from_url(url: str) -> str:
        last_slash_index = url.rfind("/")
        len_url = len(url)

        if last_slash_index < 0 or last_slash_index >= len_url - 1:
            raise MalformedUrl(f"Badly formatted url {url}")

        last_dot_index = url.rfind(".")

        if url[last_dot_index:] == ".git":
            last_suffix_index = last_dot_index
        else:
            last_suffix_index = len_url

        return url[last_slash_index + 1:last_suffix_index]


class MalformedUrl(Exception):
    def __init__(self, message):
        super().__init__(message)
