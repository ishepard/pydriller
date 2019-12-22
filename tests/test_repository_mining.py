import logging
from datetime import datetime
import tempfile
import os
import shutil
import platform

import pytest

from pydriller import RepositoryMining, GitRepository

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# It should fail when no URLs are specified
def test_no_url():
    with pytest.raises(Exception):
        list(RepositoryMining().traverse_commits())


# It should fail when URL is not a string or a List
def test_badly_formatted_repo_url():
    with pytest.raises(Exception):
        list(RepositoryMining(path_to_repo=set('repo')).traverse_commits())


def test_simple_url():
    assert len(list(RepositoryMining(
        path_to_repo="test-repos/test1").traverse_commits())) == 5


def test_two_local_urls():
    urls = ["test-repos/test1", "test-repos/test3"]
    assert len(list(RepositoryMining(
        path_to_repo=urls).traverse_commits())) == 11


def test_simple_remote_url():
    dt2 = datetime(2018, 10, 20)
    assert len(list(RepositoryMining(
        path_to_repo="https://github.com/ishepard/pydriller.git",
        to=dt2).traverse_commits())) == 159


def test_two_remote_urls():
    urls = ["https://github.com/mauricioaniche/repodriller.git",
            "https://github.com/ishepard/pydriller"]
    dt2 = datetime(2018, 10, 20)
    assert len(list(RepositoryMining(path_to_repo=urls,
                                     to=dt2).traverse_commits())) == 518


def test_2_identical_local_urls():
    urls = ["test-repos/test1", "test-repos/test1"]
    assert len(list(RepositoryMining(
        path_to_repo=urls).traverse_commits())) == 10


def test_both_local_and_remote_urls():
    dt2 = datetime(2018, 10, 20)
    assert len(list(RepositoryMining(
        path_to_repo=["test-repos/test1",
                      "https://github.com/ishepard/pydriller.git"],
        to=dt2).traverse_commits())) == 164


def test_both_local_and_remote_urls_list():
    dt2 = datetime(2018, 10, 20)
    urls = ["test-repos/test1",
            "https://github.com/mauricioaniche/repodriller.git",
            "test-repos/test3",
            "https://github.com/ishepard/pydriller.git"]
    assert len(list(RepositoryMining(path_to_repo=urls,
                                     to=dt2).traverse_commits())) == 529


def test_badly_formatted_url():
    with pytest.raises(Exception):
        list(RepositoryMining(
            path_to_repo='https://github.com/ishepard.git/test')
             .traverse_commits())

    with pytest.raises(Exception):
        list(RepositoryMining(path_to_repo='test').traverse_commits())


def test_diff_histogram():
    # without histogram
    commit = list(RepositoryMining('test-repos/test13',
                                   single="93df8676e6fab70d9677e94fd0f6b17db095e890").traverse_commits())[0]
    mod = commit.modifications[0]
    gr = GitRepository('test-repos/test13')
    diff = gr.parse_diff(mod.diff)
    assert len(diff['added']) == 11
    assert (3, '    if (path == null)') in diff['added']
    assert (5, '        log.error("Icon path is null");') in diff['added']
    assert (6, '        return null;') in diff['added']
    assert (8, '') in diff['added']
    assert (9, '    java.net.URL imgURL = GuiImporter.class.getResource(path);') in diff['added']
    assert (10, '') in diff['added']
    assert (11, '    if (imgURL == null)') in diff['added']
    assert (12, '    {') in diff['added']
    assert (14, '        return null;') in diff['added']
    assert (16, '    else') in diff['added']
    assert (17, '        return new ImageIcon(imgURL);') in diff['added']

    assert len(diff['deleted']) == 7
    assert (3, '    java.net.URL imgURL = GuiImporter.class.getResource(path);') in diff['deleted']
    assert (4, '') in diff['deleted']
    assert (5, '    if (imgURL != null)') in diff['deleted']
    assert (7, '        return new ImageIcon(imgURL);') in diff['deleted']
    assert (9, '    else') in diff['deleted']
    assert (10, '    {') in diff['deleted']
    assert (13, '    return null;') in diff['deleted']

    # with histogram
    commit = list(RepositoryMining('test-repos/test13',
                                   single="93df8676e6fab70d9677e94fd0f6b17db095e890",
                                   histogram_diff=True).traverse_commits())[0]
    mod = commit.modifications[0]
    gr = GitRepository('test-repos/test13')
    diff = gr.parse_diff(mod.diff)
    assert (4, '    {') in diff["added"]
    assert (5, '        log.error("Icon path is null");') in diff["added"]
    assert (6, '        return null;') in diff["added"]
    assert (7, '    }') in diff["added"]
    assert (8, '') in diff["added"]
    assert (11, '    if (imgURL == null)') in diff["added"]
    assert (12, '    {') in diff["added"]
    assert (13, '        log.error("Couldn\'t find icon: " + imgURL);') in diff["added"]
    assert (14, '        return null;') in diff["added"]
    assert (17, '        return new ImageIcon(imgURL);') in diff["added"]

    assert (6, '    {') in diff["deleted"]
    assert (7, '        return new ImageIcon(imgURL);') in diff["deleted"]
    assert (10, '    {') in diff["deleted"]
    assert (11, '        log.error("Couldn\'t find icon: " + imgURL);') in diff["deleted"]
    assert (12, '    }') in diff["deleted"]
    assert (13, '    return null;') in diff["deleted"]


def test_ignore_add_whitespaces():
    commit = list(RepositoryMining('test-repos/test14',
                                   single="338a74ceae164784e216555d930210371279ba8e").traverse_commits())[0]
    assert len(commit.modifications) == 1
    commit = list(RepositoryMining('test-repos/test14',
                                   skip_whitespaces=True,
                                   single="338a74ceae164784e216555d930210371279ba8e").traverse_commits())[0]
    assert len(commit.modifications) == 0


def test_ignore_add_whitespaces_and_modified_normal_line():
    gr = GitRepository('test-repos/test14')
    commit = list(RepositoryMining('test-repos/test14',
                                   single="52716ef1f11e07308b5df1b313aec5496d5e91ce").traverse_commits())[0]
    assert len(commit.modifications) == 1
    parsed_normal_diff = gr.parse_diff(commit.modifications[0].diff)
    commit = list(RepositoryMining('test-repos/test14',
                                   skip_whitespaces=True,
                                   single="52716ef1f11e07308b5df1b313aec5496d5e91ce").traverse_commits())[0]
    assert len(commit.modifications) == 1
    parsed_wo_whitespaces_diff = gr.parse_diff(commit.modifications[0].diff)
    assert len(parsed_normal_diff['added']) == 2
    assert len(parsed_wo_whitespaces_diff['added']) == 1

    assert len(parsed_normal_diff['deleted']) == 1
    assert len(parsed_wo_whitespaces_diff['deleted']) == 0


def test_ignore_deleted_whitespaces():
    commit = list(RepositoryMining('test-repos/test14',
                                   single="e6e429f6b485e18fb856019d9953370fd5420b20").traverse_commits())[0]
    assert len(commit.modifications) == 1
    commit = list(RepositoryMining('test-repos/test14',
                                   skip_whitespaces=True,
                                   single="e6e429f6b485e18fb856019d9953370fd5420b20").traverse_commits())[0]
    assert len(commit.modifications) == 0


def test_ignore_add_whitespaces_and_changed_file():
    commit = list(RepositoryMining('test-repos/test14',
                                   single="532068e9d64b8a86e07eea93de3a57bf9e5b4ae0").traverse_commits())[0]
    assert len(commit.modifications) == 2
    commit = list(RepositoryMining('test-repos/test14',
                                   skip_whitespaces=True,
                                   single="532068e9d64b8a86e07eea93de3a57bf9e5b4ae0").traverse_commits())[0]
    assert len(commit.modifications) == 1


@pytest.mark.skipif(platform.system() == "Windows", reason="Sometimes Windows give an error 'Handle is not valid' in this test, though it works anyway outside the test.")
def test_clone_repo_to():
    tmp_folder = tempfile.TemporaryDirectory()
    dt2 = datetime(2018, 10, 20)
    url = "https://github.com/ishepard/pydriller.git"
    assert len(list(RepositoryMining(
        path_to_repo=url,
        to=dt2,
        clone_repo_to=tmp_folder.name).traverse_commits())) == 159
