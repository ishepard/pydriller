import logging
from datetime import datetime
import os
import pytest
import sys

from pydriller import Repository, Git
from pydriller.repository import MalformedUrl

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


@pytest.fixture
def repo(request):
    return list(Repository(path_to_repo=request.param).traverse_commits())


@pytest.fixture
def repo_to(request):
    path, to = request.param
    return list(Repository(path_to_repo=path, to=to).traverse_commits())


@pytest.fixture()
def git_repo(request):
    gr = Git(request.param)
    yield gr
    gr.clear()


# It should fail when no URLs are specified
def test_no_url():
    with pytest.raises(Exception):
        list(Repository().traverse_commits())


# It should fail when URL is not a string or a List
def test_badly_formatted_repo_url():
    with pytest.raises(Exception):
        list(Repository(path_to_repo=set('repo')).traverse_commits())


# It should fail when URL is malformed
def test_malformed_url():
    with pytest.raises(MalformedUrl):
        list(Repository("https://badurl.git/").traverse_commits())


@pytest.mark.parametrize('repo,expected', [
    ("test-repos/small_repo", 5)
], indirect=['repo'])
def test_simple_url(repo, expected):
    assert len(repo) == expected


@pytest.mark.parametrize('repo,expected', [
    ((["test-repos/small_repo", "test-repos/branches_merged"]), 9)
], indirect=['repo'])
def test_two_local_urls(repo, expected):
    assert len(repo) == expected


@pytest.mark.parametrize('repo_to,expected', [
    (("https://github.com/ishepard/pydriller.git", datetime(2018, 10, 20)), 159)
], indirect=['repo_to'])
def test_simple_remote_url(repo_to, expected):
    assert len(repo_to) == expected


@pytest.mark.parametrize('repo_to,expected', [
    ((["https://github.com/mauricioaniche/repodriller.git",
      "https://github.com/ishepard/pydriller"], datetime(2018, 10, 20)),
     518)
], indirect=['repo_to'])
def test_two_remote_urls(repo_to, expected):
    assert len(repo_to) == expected


@pytest.mark.parametrize('repo,expected', [
    ((["test-repos/small_repo", "test-repos/small_repo"]), 10)
], indirect=['repo'])
def test_2_identical_local_urls(repo, expected):
    assert len(repo) == expected


@pytest.mark.parametrize('repo_to,expected', [
    ((["test-repos/small_repo", "https://github.com/ishepard/pydriller.git"],
     datetime(2018, 10, 20)),
     164)
], indirect=['repo_to'])
def test_both_local_and_remote_urls(repo_to, expected):
    assert len(repo_to) == expected


@pytest.mark.parametrize('repo_to,expected', [
    ((["test-repos/small_repo", "https://github.com/mauricioaniche/repodriller.git",
      "test-repos/branches_merged", "https://github.com/ishepard/pydriller.git"],
     datetime(2018, 10, 20)),
     527)
], indirect=['repo_to'])
def test_both_local_and_remote_urls_list(repo_to, expected):
    assert len(repo_to) == expected


def test_badly_formatted_url():
    with pytest.raises(Exception):
        list(Repository(
            path_to_repo='https://github.com/ishepard.git/test')
             .traverse_commits())

    with pytest.raises(Exception):
        list(Repository(path_to_repo='test').traverse_commits())


@pytest.mark.parametrize('git_repo', ["test-repos/histogram"], indirect=True)
def test_diff_without_histogram(git_repo):
    # without histogram
    commit = list(Repository('test-repos/histogram',
                             single="93df8676e6fab70d9677e94fd0f6b17db095e890").traverse_commits())[0]

    diff = commit.modified_files[0].diff_parsed
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


@pytest.mark.parametrize('git_repo', ["test-repos/histogram"], indirect=True)
def test_diff_with_histogram(git_repo):
    # with histogram
    commit = list(Repository('test-repos/histogram',
                             single="93df8676e6fab70d9677e94fd0f6b17db095e890",
                             histogram_diff=True).traverse_commits())[0]
    diff = commit.modified_files[0].diff_parsed
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
    commit = list(Repository('test-repos/whitespace',
                             single="338a74ceae164784e216555d930210371279ba8e").traverse_commits())[0]
    assert len(commit.modified_files) == 1
    commit = list(Repository('test-repos/whitespace',
                             skip_whitespaces=True,
                             single="338a74ceae164784e216555d930210371279ba8e").traverse_commits())[0]
    assert len(commit.modified_files) == 0


@pytest.mark.parametrize('git_repo', ["test-repos/whitespace"], indirect=True)
def test_ignore_add_whitespaces_and_modified_normal_line(git_repo):
    commit = list(Repository('test-repos/whitespace',
                             single="52716ef1f11e07308b5df1b313aec5496d5e91ce").traverse_commits())[0]
    assert len(commit.modified_files) == 1
    parsed_normal_diff = commit.modified_files[0].diff_parsed
    commit = list(Repository('test-repos/whitespace',
                             skip_whitespaces=True,
                             single="52716ef1f11e07308b5df1b313aec5496d5e91ce").traverse_commits())[0]
    assert len(commit.modified_files) == 1
    parsed_wo_whitespaces_diff = commit.modified_files[0].diff_parsed
    assert len(parsed_normal_diff['added']) == 2
    assert len(parsed_wo_whitespaces_diff['added']) == 1

    assert len(parsed_normal_diff['deleted']) == 1
    assert len(parsed_wo_whitespaces_diff['deleted']) == 0


def test_ignore_deleted_whitespaces():
    commit = list(Repository('test-repos/whitespace',
                             single="e6e429f6b485e18fb856019d9953370fd5420b20").traverse_commits())[0]
    assert len(commit.modified_files) == 1
    commit = list(Repository('test-repos/whitespace',
                             skip_whitespaces=True,
                             single="e6e429f6b485e18fb856019d9953370fd5420b20").traverse_commits())[0]
    assert len(commit.modified_files) == 0


def test_ignore_add_whitespaces_and_changed_file():
    commit = list(Repository('test-repos/whitespace',
                             single="532068e9d64b8a86e07eea93de3a57bf9e5b4ae0").traverse_commits())[0]
    assert len(commit.modified_files) == 2
    commit = list(Repository('test-repos/whitespace',
                             skip_whitespaces=True,
                             single="532068e9d64b8a86e07eea93de3a57bf9e5b4ae0").traverse_commits())[0]
    assert len(commit.modified_files) == 1


def test_clone_repo_to(tmp_path):
    dt2 = datetime(2018, 10, 20)
    url = "https://github.com/ishepard/pydriller.git"
    assert len(list(Repository(
        path_to_repo=url,
        to=dt2,
        clone_repo_to=str(tmp_path)).traverse_commits())) == 159
    assert tmp_path.exists() is True


def test_clone_repo_to_not_existing():
    with pytest.raises(Exception):
        list(Repository("https://github.com/ishepard/pydriller",
                        clone_repo_to="NOTEXISTINGDIR").traverse_commits())


def test_clone_repo_to_repeated():
    import tempfile
    tmp_path = tempfile.gettempdir()
    dt2 = datetime(2018, 10, 20)
    url = "https://github.com/ishepard/pydriller.git"
    assert len(list(Repository(
        path_to_repo=url,
        to=dt2,
        clone_repo_to=str(tmp_path)).traverse_commits())) == 159
    assert os.path.isdir(os.path.join(tmp_path, "pydriller"))
    assert len(list(Repository(
        path_to_repo=url,
        to=dt2,
        clone_repo_to=str(tmp_path)).traverse_commits())) == 159
    assert os.path.isdir(os.path.join(tmp_path, "pydriller"))


def test_projectname_multiple_repos():
    repos = [
        'test-repos/files_in_directories',
        'test-repos/files_in_directories',
        'test-repos/files_in_directories'
    ]
    for commit in Repository(path_to_repo=repos).traverse_commits():
        assert commit.project_name == 'files_in_directories'


def test_projectname_multiple_repos_remote():
    repos = [
        'https://github.com/ishepard/pydriller',
        'test-repos/pydriller'
    ]
    for commit in Repository(path_to_repo=repos).traverse_commits():
        assert commit.project_name == 'pydriller'


@pytest.mark.skipif(sys.version_info < (3, 8) and sys.platform == "win32", reason="requires Python3.8 or greater on Windows")
def test_deletion_remotes():
    repos = [
        'https://github.com/ishepard/pydriller',
        'https://github.com/ishepard/pydriller'
    ]
    paths = set()
    for commit in Repository(path_to_repo=repos).traverse_commits():
        paths.add(commit.project_path)

    for path in paths:
        assert os.path.exists(path) is False


def test_deleted_files():
    deleted_commits = list(
        Repository('https://github.com/ishepard/pydriller',
                   filepath='.bettercodehub.yml',
                   include_deleted_files=True).traverse_commits()
    )
    assert len(deleted_commits) > 0
