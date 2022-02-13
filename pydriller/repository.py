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
from typing import List, Generator, Union

from git import Repo

from pydriller.domain.commit import Commit
from pydriller.git import Git
from pydriller.utils.conf import Conf

logger = logging.getLogger(__name__)


class Repository:
    """
    This is the main class of PyDriller, responsible for running the study.
    """

    def __init__(self, path_to_repo: Union[str, List[str]],
                 single: str = None,
                 since: datetime = None, to: datetime = None,
                 from_commit: str = None, to_commit: str = None,
                 from_tag: str = None, to_tag: str = None,
                 include_refs: bool = False,
                 include_remotes: bool = False,
                 num_workers: int = 1,
                 only_in_branch: str = None,
                 only_modifications_with_file_types: List[str] = None,
                 only_no_merge: bool = False,
                 only_authors: List[str] = None,
                 only_commits: List[str] = None,
                 only_releases: bool = False,
                 filepath: str = None,
                 include_deleted_files: bool = False,
                 histogram_diff: bool = False,
                 skip_whitespaces: bool = False,
                 clone_repo_to: str = None,
                 order: str = None):
        """
        Init a repository. The only required parameter is
        "path_to_repo": to analyze a single repo, pass the absolute path to
        the repo; if you need to analyze more repos, pass a list of absolute
        paths.

        Furthermore, PyDriller supports local and remote repositories: if
        you pass a path to a repo, PyDriller will run the study on that
        repo; if you pass an URL, PyDriller will clone the repo in a
        temporary folder, run the study, and delete the temporary folder.

        :param Union[str,List[str]] path_to_repo: absolute path (or list of
            absolute paths) to the repository(ies) to analyze
        :param str single: hash of a single commit to analyze
        :param datetime since: starting date
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
        :param bool clone_repo_to: if the repo under analysis is remote, clone the repo to the specified directory
        :param str filepath: only commits that modified this file will be analyzed
        :param bool include_deleted_files: include commits modifying a deleted file (useful when analyzing a deleted `filepath`)
        :param str order: order of commits. It can be one of: 'date-order',
            'author-date-order', 'topo-order', or 'reverse'. Default is reverse.
        """
        file_modification_set = (
            None if only_modifications_with_file_types is None
            else set(only_modifications_with_file_types)
            )
        commit_set = (
            None if only_commits is None
            else set(only_commits)
            )

        options = {
            "git": None,
            "path_to_repo": path_to_repo,
            "from_commit": from_commit,
            "to_commit": to_commit,
            "from_tag": from_tag,
            "to_tag": to_tag,
            "since": since,
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
            "order": order
        }
        self._conf = Conf(options)

        # If the user provides a directory where to clone the repositories,
        # make sure we do not delete the directory after the study completes
        self._cleanup = False if clone_repo_to is not None else True

    @staticmethod
    def _is_remote(repo: str) -> bool:
        return repo.startswith(("git@", "https://", "http://"))

    def _clone_remote_repo(self, tmp_folder: str, repo: str) -> str:
        repo_folder = os.path.join(tmp_folder, self._get_repo_name_from_url(repo))
        if os.path.isdir(repo_folder):
            logger.info(f"Reusing folder {repo_folder} for {repo}")
        else:
            logger.info(f"Cloning {repo} in temporary folder {repo_folder}")
            Repo.clone_from(url=repo, to_path=repo_folder)

        return repo_folder

    def _clone_folder(self) -> str:
        if self._conf.get('clone_repo_to'):
            clone_folder = str(Path(self._conf.get('clone_repo_to')))
            if not os.path.isdir(clone_folder):
                raise Exception("Not a directory: {0}".format(clone_folder))
        else:
            # Save the temporary directory so we can clean it up later
            self._tmp_dir = tempfile.TemporaryDirectory()
            clone_folder = self._tmp_dir.name
        return clone_folder

    @contextmanager
    def _prep_repo(self, path_repo: str) -> Generator[Git, None, None]:
        local_path_repo = path_repo
        if self._is_remote(path_repo):
            local_path_repo = self._clone_remote_repo(self._clone_folder(), path_repo)
        local_path_repo = str(Path(local_path_repo).expanduser().resolve())

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
            except PermissionError:
                # on Windows, Python 3.5, 3.6, 3.7 are not able to delete
                # git directories because of read-only files.
                # In this case, just ignore the errors.
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

                commits_list = list(git.get_list_commits(rev, **kwargs))

                if not commits_list:
                    return

                chunks = self._split_in_chunks(commits_list, self._conf.get("num_workers"))
                with concurrent.futures.ThreadPoolExecutor(max_workers=self._conf.get("num_workers")) as executor:
                    jobs = {executor.submit(self._iter_commits, chunk): chunk for chunk in chunks}

                    for job in concurrent.futures.as_completed(jobs):
                        for commit in job.result():
                            yield commit

    def _iter_commits(self, commits_list: List[Commit]) -> Generator[Commit, None, None]:
        for commit in commits_list:
            logger.info(f'Commit #{commit.hash} in {commit.committer_date} from {commit.author.name}')

            if self._conf.is_commit_filtered(commit):
                logger.info(f'Commit #{commit.hash} filtered')
                continue

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
        last_suffix_index = url.rfind(".git")
        if last_suffix_index < 0:
            last_suffix_index = len(url)

        if last_slash_index < 0 or last_suffix_index <= last_slash_index:
            raise MalformedUrl(f"Badly formatted url {url}")

        return url[last_slash_index + 1:last_suffix_index]


class MalformedUrl(Exception):
    def __init__(self, message):
        super().__init__(message)
