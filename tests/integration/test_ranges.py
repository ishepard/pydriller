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

from pydriller.repository_mining import RepositoryMining
from datetime import datetime, timezone, timedelta
import logging
import pytest

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


to_zone = timezone(timedelta(hours=1))
dt = datetime(2018, 3, 22, 10, 41, 30, tzinfo=to_zone)
dt1 = datetime(2018, 3, 22, 10, 41, 45, tzinfo=to_zone)
dt2 = datetime(2018, 3, 22, 10, 42, 3, tzinfo=to_zone)
to_zone = timezone(timedelta(hours=2))
dt3 = datetime(2018, 3, 27, 17, 20, 3, tzinfo=to_zone)


@pytest.fixture
def path():
    return 'test-repos/small_repo/'


@pytest.fixture
def since():
    return None


@pytest.fixture
def to():
    return None


@pytest.fixture
def from_commit():
    return None


@pytest.fixture
def to_commit():
    return None


@pytest.fixture
def from_tag():
    return None


@pytest.fixture
def to_tag():
    return None


@pytest.fixture
def repository_mining_st(path, since, to):
    return list(RepositoryMining(path, since=since, to=to).traverse_commits())


@pytest.fixture
def repository_mining_cc(path, from_commit, to_commit):
    return list(RepositoryMining(path, from_commit=from_commit, to_commit=to_commit).traverse_commits())


@pytest.fixture
def repository_mining_tt(path, from_tag, to_tag):
    return list(RepositoryMining(path, from_tag=from_tag, to_tag=to_tag).traverse_commits())


@pytest.fixture
def repository_mining_complex_tags(path, from_tag, to_tag):
    return list(RepositoryMining('test-repos/tags',
                                 from_tag=from_tag,
                                 to_tag=to_tag).traverse_commits())


@pytest.mark.parametrize('to,expected_commits', [
    (None, 5),
    (dt, 1),
    (dt1, 1),
    (dt2, 3),
    (dt3, 4),
])
def test_to_filter(repository_mining_st, expected_commits):
    assert len(repository_mining_st) == expected_commits


@pytest.mark.parametrize('since,expected_commits', [
    (None, 5),
    (dt, 4),
    (dt1, 4),
    (dt2, 3),
    (dt3, 1),
])
def test_since_filter(repository_mining_st, expected_commits):
    assert len(repository_mining_st) == expected_commits


@pytest.mark.parametrize('since,to,expected_commits', [
    (dt1, dt3, 3),
    (dt, dt3, 3),
    (dt2, dt3, 2),
])
def test_since_and_to_filters(repository_mining_st, expected_commits):
    assert len(repository_mining_st) == expected_commits


# FROM AND TO COMMIT
@pytest.mark.parametrize('to_commit,expected_commits', [
    ('6411e3096dd2070438a17b225f44475136e54e3a', 2),
    ('09f6182cef737db02a085e1d018963c7a29bde5a', 3),
    ('1f99848edadfffa903b8ba1286a935f1b92b2845', 4),
    ('HEAD', 5),
])
def test_to_commit_filter(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


@pytest.mark.parametrize('from_commit,expected_commits', [
    ('6411e3096dd2070438a17b225f44475136e54e3a', 4),
    ('09f6182cef737db02a085e1d018963c7a29bde5a', 3),
    ('1f99848edadfffa903b8ba1286a935f1b92b2845', 2),
    ('HEAD', 1)
])
def test_from_commit_filter(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


@pytest.mark.parametrize('from_commit,to_commit,expected_commits', [
    ('6411e3096dd2070438a17b225f44475136e54e3a', '09f6182cef737db02a085e1d018963c7a29bde5a', 2),
    ('09f6182cef737db02a085e1d018963c7a29bde5a', '6411e3096dd2070438a17b225f44475136e54e3a', 2),
    ('6411e3096dd2070438a17b225f44475136e54e3a', 'HEAD', 4),
    ('09f6182cef737db02a085e1d018963c7a29bde5a', 'HEAD', 3),
])
def test_from_and_to_commit(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


def test_from_and_to_commit_with_merge_commit():
    commits = RepositoryMining('test-repos/pydriller',
                               from_commit="015f7144641a418f6a9fae4d024286ec17fd7ce8",
                               to_commit="01d2f2fbeb6980cc5568825d008017ca8ca767d6").traverse_commits()
    assert len(list(commits)) == 3


# FROM AND TO TAG
@pytest.mark.parametrize('to_tag,expected_commits', [
    ('v1.4', 3),
])
def test_to_tag_filter_new(repository_mining_tt, expected_commits):
    assert len(repository_mining_tt) == expected_commits


@pytest.mark.parametrize('from_tag,expected_commits', [
    ('v1.4', 3),
])
def test_from_tag_filter(repository_mining_tt, expected_commits):
    assert len(repository_mining_tt) == expected_commits


@pytest.mark.parametrize('from_tag,to_tag,expected_commits', [
    ('tag1', 'tag2', 3),
    ('tag1', 'tag3', 5),
    ('tag2', 'tag3', 3),
])
def test_from_and_to_tag(repository_mining_complex_tags, expected_commits):
    assert len(repository_mining_complex_tags) == expected_commits


def test_multiple_filters_exceptions():
    from_commit = '6411e3096dd2070438a17b225f44475136e54e3a'
    from_tag = 'v1.4'

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/small_repo/',
                                       since=dt1,
                                       from_commit=from_commit
                                       ).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/small_repo/',
                                       since=dt1,
                                       from_tag=from_tag).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/small_repo/',
                                       from_commit=from_commit,
                                       from_tag=from_tag).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/small_repo/',
                                       to=dt1,
                                       to_commit=from_commit
                                       ).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/small_repo/',
                                       to=dt1,
                                       to_tag=from_tag).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/small_repo/',
                                       single=from_commit,
                                       to=dt1,
                                       to_tag=from_tag).traverse_commits():
            print(commit.hash)
