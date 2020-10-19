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
This module includes common functions.
"""
import logging
import os
import shutil
import stat
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import List, Generator

from git import Repo

from pydriller.utils.conf import Conf

logger = logging.getLogger(__name__)


def get_files(path: str) -> List[str]:
    """
    Obtain the list of the files (excluding .git directory).

    :return: List[str], the list of the files
    """
    _all = []
    for path, _, files in os.walk(path):
        if '.git' in path:
            continue
        for name in files:
            _all.append(os.path.join(path, name))
    return _all


def is_remote(repo: str) -> bool:
    """
    Return true if the repo is remote

    :param repo: string of the repo
    :return: bool
    """
    return repo.startswith("git@") or repo.startswith("https://")


def clone_remote_repo(tmp_folder: str, repo: str) -> str:
    """
    Clone the repository when it is remote.
    :param tmp_folder:
    :param repo:
    :return:
    """
    repo_folder = os.path.join(tmp_folder, get_repo_name_from_url(repo))
    logger.info("Cloning %s in temporary folder %s", repo, repo_folder)
    Repo.clone_from(url=repo, to_path=repo_folder)

    return repo_folder


def get_repo_name_from_url(url: str) -> str:
    """
    Return the name of the repository, that is "pydriller" in "https://github.com/ishepard/pydriller"
    :param url: url of the repository
    :return:
    """
    last_slash_index = url.rfind("/")
    last_suffix_index = url.rfind(".git")
    if last_suffix_index < 0:
        last_suffix_index = len(url)

    if last_slash_index < 0 or last_suffix_index <= last_slash_index:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash_index + 1:last_suffix_index]


@contextmanager
def open_folder(path_repo: str, conf: Conf, cleanup: bool) -> Generator[str, None, None]:
    """
    Function responsible of preparing the folder with the reposutory
    and cleaning it after Pydriller finish the study.

    :param path_repo:
    :param conf:
    :param cleanup:
    :return:
    """
    local_path_repo = path_repo
    tmp_dir = None

    if is_remote(path_repo):
        if conf.get('clone_repo_to'):
            clone_folder = str(Path(conf.get('clone_repo_to')))
            if not os.path.isdir(clone_folder):
                raise Exception("Not a directory: {0}".format(clone_folder))
        else:
            # Save the temporary directory so we can clean it up later
            tmp_dir = tempfile.TemporaryDirectory()
            clone_folder = tmp_dir.name
        local_path_repo = clone_remote_repo(clone_folder, path_repo)
    local_path_repo = str(Path(local_path_repo).expanduser().resolve())

    yield local_path_repo

    # delete the temporary directory if created
    if is_remote(path_repo) and cleanup is True:
        assert tmp_dir is not None
        try:
            tmp_dir.cleanup()
        except PermissionError:
            # on Windows, Python 3.5, 3.6, 3.7 are not able to delete
            # git directories because of read-only files. This is now fixed
            # in python 3.8. In this case, we need to use an
            # onerror callback to clear the read-only bit.
            # see https://docs.python.org/3/library/shutil.html?highlight=shutil#rmtree-example
            def _remove_readonly(func, path, _):
                os.chmod(path, stat.S_IWRITE)
                func(path)

            shutil.rmtree(tmp_dir.name, onerror=_remove_readonly)
