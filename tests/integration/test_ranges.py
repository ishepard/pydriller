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
def repository_mining_st(request):
    since, to = request.param
    return list(RepositoryMining('test-repos/small_repo/', since=since, to=to).traverse_commits())


@pytest.fixture
def repository_mining_cc(request):
    from_commit, to_commit = request.param
    return list(RepositoryMining('test-repos/small_repo/', from_commit=from_commit, to_commit=to_commit).traverse_commits())


@pytest.fixture
def repository_mining_tt(request):
    from_tag, to_tag = request.param
    return list(RepositoryMining('test-repos/small_repo/', from_tag=from_tag, to_tag=to_tag).traverse_commits())


@pytest.fixture
def repository_mining_complex_tags(request):
    from_tag, to_tag = request.param
    return list(RepositoryMining('test-repos/tags',
                                 from_tag=from_tag,
                                 to_tag=to_tag).traverse_commits())


@pytest.mark.parametrize('repository_mining_st,expected_commits', [
    ((None, None), 5),
    ((None, dt), 1),
    ((None, dt1), 1),
    ((None, dt2), 3),
    ((None, dt3), 4),
], indirect=['repository_mining_st'])
def test_to_filter(repository_mining_st, expected_commits):
    assert len(repository_mining_st) == expected_commits


@pytest.mark.parametrize('repository_mining_st,expected_commits', [
    ((None, None), 5),
    ((dt, None), 4),
    ((dt1, None), 4),
    ((dt2, None), 3),
    ((dt3, None), 1),
], indirect=['repository_mining_st'])
def test_since_filter(repository_mining_st, expected_commits):
    assert len(repository_mining_st) == expected_commits


@pytest.mark.parametrize('repository_mining_st,expected_commits', [
    ((dt1, dt3), 3),
    ((dt, dt3), 3),
    ((dt2, dt3), 2),
], indirect=['repository_mining_st'])
def test_since_and_to_filters(repository_mining_st, expected_commits):
    assert len(repository_mining_st) == expected_commits


# FROM AND TO COMMIT
@pytest.mark.parametrize('repository_mining_cc,expected_commits', [
    ((None, '6411e3096dd2070438a17b225f44475136e54e3a'), 2),
    ((None, '09f6182cef737db02a085e1d018963c7a29bde5a'), 3),
    ((None, '1f99848edadfffa903b8ba1286a935f1b92b2845'), 4),
    ((None, 'HEAD'), 5),
], indirect=['repository_mining_cc'])
def test_to_commit_filter(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


@pytest.mark.parametrize('repository_mining_cc,expected_commits', [
    (('6411e3096dd2070438a17b225f44475136e54e3a', None), 4),
    (('09f6182cef737db02a085e1d018963c7a29bde5a', None), 3),
    (('1f99848edadfffa903b8ba1286a935f1b92b2845', None), 2),
    (('HEAD', None), 1)
], indirect=['repository_mining_cc'])
def test_from_commit_filter(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


@pytest.mark.parametrize('repository_mining_cc,expected_commits', [
    (('6411e3096dd2070438a17b225f44475136e54e3a', '09f6182cef737db02a085e1d018963c7a29bde5a'), 2),
    (('09f6182cef737db02a085e1d018963c7a29bde5a', '6411e3096dd2070438a17b225f44475136e54e3a'), 2),
    (('6411e3096dd2070438a17b225f44475136e54e3a', 'HEAD'), 4),
    (('09f6182cef737db02a085e1d018963c7a29bde5a', 'HEAD'), 3),
], indirect=['repository_mining_cc'])
def test_from_and_to_commit(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


def test_from_and_to_commit_with_merge_commit():
    commits = RepositoryMining('test-repos/pydriller',
                               from_commit="015f7144641a418f6a9fae4d024286ec17fd7ce8",
                               to_commit="01d2f2fbeb6980cc5568825d008017ca8ca767d6").traverse_commits()
    assert len(list(commits)) == 3


# FROM AND TO TAG
@pytest.mark.parametrize('repository_mining_tt,expected_commits', [
    ((None, 'v1.4'), 3),
], indirect=['repository_mining_tt'])
def test_to_tag_filter_new(repository_mining_tt, expected_commits):
    assert len(repository_mining_tt) == expected_commits


@pytest.mark.parametrize('repository_mining_tt,expected_commits', [
    (('v1.4', None), 3),
], indirect=['repository_mining_tt'])
def test_from_tag_filter(repository_mining_tt, expected_commits):
    assert len(repository_mining_tt) == expected_commits


@pytest.mark.parametrize('repository_mining_complex_tags,expected_commits', [
    (('tag1', 'tag2'), 3),
    (('tag1', 'tag3'), 5),
    (('tag2', 'tag3'), 3),
], indirect=['repository_mining_complex_tags'])
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
