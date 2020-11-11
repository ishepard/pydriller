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
This module includes 1 class, RepositoryMining, main class of PyDriller.
"""

import logging
import os
import shutil
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import List, Generator, Union

from git import Repo

from pydriller.domain.commit import Commit
from pydriller.git_repository import GitRepository
from pydriller.utils.conf import Conf

logger = logging.getLogger(__name__)


class RepositoryMining:
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
                 only_in_branch: str = None,
                 only_modifications_with_file_types: List[str] = None,
                 only_no_merge: bool = False,
                 only_authors: List[str] = None,
                 only_commits: List[str] = None,
                 only_releases: bool = False,
                 filepath: str = None,
                 histogram_diff: bool = False,
                 skip_whitespaces: bool = False,
                 clone_repo_to: str = None,
                 order: str = None):
        """
        Init a repository mining. The only required parameter is
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
            "git_repo": None,
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
            "only_in_branch": only_in_branch,
            "only_modifications_with_file_types": file_modification_set,
            "only_no_merge": only_no_merge,
            "only_authors": only_authors,
            "only_commits": commit_set,
            "only_releases": only_releases,
            "skip_whitespaces": skip_whitespaces,
            "filepath": filepath,
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
        return repo.startswith("git@") or repo.startswith("https://")

    def _clone_remote_repo(self, tmp_folder: str, repo: str) -> str:
        repo_folder = os.path.join(tmp_folder, self._get_repo_name_from_url(repo))
        logger.info("Cloning %s in temporary folder %s", repo, repo_folder)
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
    def _prep_repo(self, path_repo: str) -> Generator[GitRepository, None, None]:
        local_path_repo = path_repo
        if self._is_remote(path_repo):
            local_path_repo = self._clone_remote_repo(self._clone_folder(), path_repo)
        local_path_repo = str(Path(local_path_repo).expanduser().resolve())

        # when multiple repos are given in input, this variable will serve as a reminder
        # of which one we are currently analyzing
        self._conf.set_value('path_to_repo', local_path_repo)

        self.git_repo = GitRepository(local_path_repo, self._conf)
        # saving the GitRepository object for further use
        self._conf.set_value("git_repo", self.git_repo)

        # checking that the filters are set correctly
        self._conf.sanity_check_filters()
        yield self.git_repo

        # cleaning, this is necessary since GitPython issues on memory leaks
        self._conf.set_value("git_repo", None)
        self.git_repo.clear()
        self.git_repo = None  # type: ignore

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
            with self._prep_repo(path_repo=path_repo) as git_repo:
                logger.info('Analyzing git repository in %s', git_repo.path)

                # Get the commits that modified the filepath. In this case, we can not use
                # git rev-list since it doesn't have the option --follow, necessary to follow
                # the renames. Hence, we manually call git log instead
                if self._conf.get('filepath') is not None:
                    self._conf.set_value('filepath_commits', git_repo.get_commits_modified_file(self._conf.get('filepath')))

                # Gets only the commits that are tagged
                if self._conf.get('only_releases'):
                    self._conf.set_value('tagged_commits', git_repo.get_tagged_commits())

                # Build the arguments to pass to git rev-list.
                rev, kwargs = self._conf.build_args()

                # Iterate over all the commits returned by git rev-list
                for commit in git_repo.get_list_commits(rev, **kwargs):
                    logger.info('Commit #%s in %s from %s', commit.hash, commit.committer_date, commit.author.name)

                    if self._conf.is_commit_filtered(commit):
                        logger.info('Commit #%s filtered', commit.hash)
                        continue

                    yield commit

    @staticmethod
    def _get_repo_name_from_url(url: str) -> str:
        last_slash_index = url.rfind("/")
        last_suffix_index = url.rfind(".git")
        if last_suffix_index < 0:
            last_suffix_index = len(url)

        if last_slash_index < 0 or last_suffix_index <= last_slash_index:
            raise Exception("Badly formatted url {}".format(url))

        return url[last_slash_index + 1:last_suffix_index]
