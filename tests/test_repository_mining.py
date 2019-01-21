import logging
from datetime import datetime

import pytest

from pydriller import RepositoryMining

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


# It should fail when no URLs are specified
def test_no_url():
    with pytest.raises(Exception):
        list(RepositoryMining().traverse_commits())


# It should fail when URL is not a string or a List
def test_badly_formatted_repo_url():
    with pytest.raises(Exception):
        list(RepositoryMining(path_to_repo=set('repo')).traverse_commits())


def test_simple_url():
    assert len(list(RepositoryMining(path_to_repo="test-repos/test1").traverse_commits())) == 5


def test_two_local_urls():
    urls = ["test-repos/test1", "test-repos/test3"]
    assert len(list(RepositoryMining(path_to_repo=urls).traverse_commits())) == 11


def test_simple_remote_url():
    dt2 = datetime(2018, 10, 20)
    assert len(list(
        RepositoryMining(path_to_repo="https://github.com/ishepard/pydriller.git", to=dt2).traverse_commits())) == 159


def test_two_remote_urls():
    urls = ["https://github.com/mauricioaniche/repodriller.git", "https://github.com/ishepard/pydriller"]
    dt2 = datetime(2018, 10, 20)
    assert len(list(RepositoryMining(path_to_repo=urls, to=dt2).traverse_commits())) == 518


def test_2_identical_local_urls():
    urls = ["test-repos/test1", "test-repos/test1"]
    assert len(list(RepositoryMining(path_to_repo=urls).traverse_commits())) == 10


def test_both_local_and_remote_urls():
    dt2 = datetime(2018, 10, 20)
    assert len(list(RepositoryMining(path_to_repo=["test-repos/test1", "https://github.com/ishepard/pydriller.git"],
                                     to=dt2).traverse_commits())) == 164


def test_both_local_and_remote_urls_list():
    dt2 = datetime(2018, 10, 20)
    urls = ["test-repos/test1", "https://github.com/mauricioaniche/repodriller.git", "test-repos/test3",
            "https://github.com/ishepard/pydriller.git"]
    assert len(list(RepositoryMining(path_to_repo=urls, to=dt2).traverse_commits())) == 529


def test_badly_formatted_url():
    with pytest.raises(Exception):
        list(RepositoryMining(path_to_repo='https://github.com/ishepard.git/test').traverse_commits())

    with pytest.raises(Exception):
        list(RepositoryMining(path_to_repo='test').traverse_commits())


def test_filepath_with_to():
    dt = datetime(2018, 6, 6)
    assert len(list(RepositoryMining(
        path_to_repo='test-repos/test5',
        filepath='A.java',
        to=dt).traverse_commits())) == 4


def test_filepath_with_since():
    since = datetime(2018, 6, 6)
    assert len(list(RepositoryMining(
        path_to_repo='test-repos/test5',
        filepath='A.java',
        since=since).traverse_commits())) == 7


def test_filepath_with_rename():
    dt = datetime(2018, 6, 6)
    commits = list(RepositoryMining(
        path_to_repo='test-repos/test1',
        filepath='file4.java',
        to=dt).traverse_commits())
    assert len(commits) == 2

    commit_hashes = [commit.hash for commit in commits]

    assert 'da39b1326dbc2edfe518b90672734a08f3c13458' in commit_hashes
    assert 'a88c84ddf42066611e76e6cb690144e5357d132c' in commit_hashes


def test_filepath_with_rename_complex():
    commits = list(RepositoryMining(
        path_to_repo='test-repos/git-1',
        filepath='Matricula.javax').traverse_commits())
    assert len(commits) == 6

    commit_hashes = [commit.hash for commit in commits]

    assert 'f0dd1308bd904a9b108a6a40865166ee962af3d4' in commit_hashes
    assert '953737b199de233896f00b4d87a0bc2794317253' in commit_hashes
    assert 'a3290ac2f555eabca9e31180cf38e91f9e7e2761' in commit_hashes
    assert '71535a31f0b598a5d5fcebda7146ebc01def783a' in commit_hashes
    assert '57dbd017d1a744b949e7ca0b1c1a3b3dd4c1cbc1' in commit_hashes
    assert '866e997a9e44cb4ddd9e00efe49361420aff2559' in commit_hashes
