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

import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

import pytest
from pydriller.repository_mining import RepositoryMining
from datetime import datetime, timezone, timedelta

to_zone = timezone(timedelta(hours=1))
dt = datetime(2018, 3, 22, 10, 41, 30, tzinfo=to_zone)
dt1 = datetime(2018, 3, 22, 10, 42, 3, tzinfo=to_zone)
dt2 = datetime(2018, 3, 22, 10, 41, 45, tzinfo=to_zone)
to_zone = timezone(timedelta(hours=2))
dt3 = datetime(2018, 3, 27, 17, 20, 3, tzinfo=to_zone)


@pytest.fixture
def path():
    return 'test-repos/test1/'


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


@pytest.mark.parametrize('to,expected_commits', [
    (None, 5),
    (dt1, 3),
])
def test_to_filter(repository_mining_st, expected_commits):
    assert len(repository_mining_st) == expected_commits


@pytest.mark.parametrize('since,expected_commits', [
    (None, 5),
    (dt, 4),
])
def test_since_filter(repository_mining_st, expected_commits):
    assert len(repository_mining_st) == expected_commits


@pytest.mark.parametrize('since,to,expected_commits', [
    (dt2, dt3, 3),
])
def test_since_and_to_filters(repository_mining_st, expected_commits):
    assert len(repository_mining_st) == expected_commits


# FROM AND TO COMMIT
@pytest.mark.parametrize('to_commit,expected_commits', [
    ('09f6182cef737db02a085e1d018963c7a29bde5a', 3),
])
def test_to_commit_filter_new(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


@pytest.mark.parametrize('from_commit,expected_commits', [
    ('6411e3096dd2070438a17b225f44475136e54e3a', 4),
])
def test_from_commit_filter(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


@pytest.mark.parametrize('from_commit,to_commit,expected_commits', [
    ('6411e3096dd2070438a17b225f44475136e54e3a', '09f6182cef737db02a085e1d018963c7a29bde5a', 2),
])
def test_from_and_to_commit(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


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
    ('v1.4', 'v1.4', 1),
])
def test_from_and_to_tag(repository_mining_tt, expected_commits):
    assert len(repository_mining_tt) == expected_commits


def test_multiple_filters_exceptions():
    from_commit = '6411e3096dd2070438a17b225f44475136e54e3a'
    from_tag = 'v1.4'

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/test1/', from_commit=from_commit,
                                       from_tag=from_tag).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/test1/', since=dt2, from_commit=from_commit).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/test1/', since=dt2, from_tag=from_tag).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/test1/', to=dt2, to_tag=from_tag).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/test1/', single=from_commit, to=dt2,
                                       to_tag=from_tag).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/test1/', to_commit=from_commit, to=dt2).traverse_commits():
            print(commit.hash)
