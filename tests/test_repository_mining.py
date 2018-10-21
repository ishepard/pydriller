from datetime import datetime

import pytest

from pydriller import RepositoryMining
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def test_no_url():
    with pytest.raises(Exception):
        for commit in RepositoryMining().traverse_commits():
            c = commit.hash


def test_simple_url():
    assert 5 == len(list(RepositoryMining(path_to_repo="test-repos/test1").traverse_commits()))


def test_two_local_urls():
    urls = ["test-repos/test1", "test-repos/test3"]
    assert 11 == len(list(RepositoryMining(path_to_repo=urls).traverse_commits()))


def test_simple_remote_url():
    dt2 = datetime(2018, 10, 20)
    assert 158 == len(list(RepositoryMining(path_to_remote_repo="https://github.com/ishepard/pydriller.git", to=dt2).traverse_commits()))


def test_two_remote_urls():
    urls = ["https://github.com/mauricioaniche/repodriller.git", "https://github.com/ishepard/pydriller.git"]
    dt2 = datetime(2018, 10, 20)
    assert 517 == len(list(RepositoryMining(path_to_remote_repo=urls, to=dt2).traverse_commits()))


def test_2_identical_local_urls():
    urls = ["test-repos/test1", "test-repos/test1"]
    assert 10 == len(list(RepositoryMining(path_to_repo=urls).traverse_commits()))


def test_2_identical_remote_urls():
    urls = ["https://github.com/ishepard/pydriller.git", "https://github.com/ishepard/pydriller.git"]
    dt2 = datetime(2018, 10, 20)
    with pytest.raises(Exception):
        list(RepositoryMining(path_to_remote_repo=urls, to=dt2).traverse_commits())