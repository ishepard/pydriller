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

from pydriller.repository import Repository
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
    return list(Repository('test-repos/small_repo/', since=since, to=to).traverse_commits())


@pytest.fixture
def repository_mining_cc(request):
    from_commit, to_commit = request.param
    return list(Repository('test-repos/small_repo/', from_commit=from_commit, to_commit=to_commit).traverse_commits())


@pytest.fixture
def repository_mining_cc_complex(request):
    from_commit, to_commit = request.param
    return list(Repository('test-repos/refactoring-toy-example/', from_commit=from_commit, to_commit=to_commit).traverse_commits())


@pytest.fixture
def repository_mining_tt(request):
    from_tag, to_tag = request.param
    return list(Repository('test-repos/small_repo/', from_tag=from_tag, to_tag=to_tag).traverse_commits())


@pytest.fixture
def repository_mining_complex_tags(request):
    from_tag, to_tag = request.param
    return list(Repository('test-repos/tags',
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


@pytest.mark.parametrize('repository_mining_cc_complex,expected_commits', [
    ((None, '05c1e773878bbacae64112f70964f4f2f7944398'), 9),
    ((None, '76b12f8bd6559f9ab1c830ae2b4be2afad16ec22'), 27),
    ((None, 'ef3422578c0bcaef1561980ef077d06c3f6fc9f9'), 59),
    ((None, '9a5c33b16d07d62651ea80552e8782974c96bb8a'), 64),
    ((None, 'HEAD'), 65),
], indirect=['repository_mining_cc_complex'])
def test_to_commit_filter_complex(repository_mining_cc_complex, expected_commits):
    assert len(repository_mining_cc_complex) == expected_commits


@pytest.mark.parametrize('repository_mining_cc,expected_commits', [
    (('6411e3096dd2070438a17b225f44475136e54e3a', None), 4),
    (('09f6182cef737db02a085e1d018963c7a29bde5a', None), 3),
    (('1f99848edadfffa903b8ba1286a935f1b92b2845', None), 2),
    (('HEAD', None), 1)
], indirect=['repository_mining_cc'])
def test_from_commit_filter(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


@pytest.mark.parametrize('repository_mining_cc_complex,expected_commits', [
    (('0bb0526b70870d57cbac9fcc8c4a7346a4ce5879', None), 4),
    (('1328d7873efe6caaffaf635424e19a4bb5e786a8', None), 8),
    (('5849e143567474f037950f005d994729de0775fc', None), 30),
    (('05c1e773878bbacae64112f70964f4f2f7944398', None), 56),
    (('819b202bfb09d4142dece04d4039f1708735019b', None), 65),
    (('HEAD', None), 1)
], indirect=['repository_mining_cc_complex'])
def test_from_commit_filter_complex(repository_mining_cc_complex, expected_commits):
    assert len(repository_mining_cc_complex) == expected_commits


@pytest.mark.parametrize('repository_mining_cc,expected_commits', [
    (('6411e3096dd2070438a17b225f44475136e54e3a', '09f6182cef737db02a085e1d018963c7a29bde5a'), 2),
    (('09f6182cef737db02a085e1d018963c7a29bde5a', '6411e3096dd2070438a17b225f44475136e54e3a'), 2),
    (('6411e3096dd2070438a17b225f44475136e54e3a', 'HEAD'), 4),
    (('09f6182cef737db02a085e1d018963c7a29bde5a', 'HEAD'), 3),
], indirect=['repository_mining_cc'])
def test_from_and_to_commit(repository_mining_cc, expected_commits):
    assert len(repository_mining_cc) == expected_commits


@pytest.mark.parametrize('repository_mining_cc_complex,expected_commits', [
    (('cd61fd2a70828030ccb3cf46d8719f8b204c52ed', 'e78b02fe027621aec1227cbf5555c75775ba296b'), 6),
    (('40950c317bd52ea5ce4cf0d19707fe426b66649c', '3bfbc107eac92f388de9f8b87682c3a0baf74981'), 10),
    (('e78b02fe027621aec1227cbf5555c75775ba296b', 'e6237f795546c5f14765330ceebe44cd41cdfffe'), 45),
    (('cd61fd2a70828030ccb3cf46d8719f8b204c52ed', '9a5c33b16d07d62651ea80552e8782974c96bb8a'), 63),
], indirect=['repository_mining_cc_complex'])
def test_from_and_to_commit_complex(repository_mining_cc_complex, expected_commits):
    assert len(repository_mining_cc_complex) == expected_commits


@pytest.mark.parametrize('repository_mining_cc_complex,expected_commits', [
    (('c286db365e7374fe4d08f54077abb7fba81dd296', None), 5),
    (('e6237f795546c5f14765330ceebe44cd41cdfffe', None), 10),
    (('b95891f09907aaa0c6dfc6012a7b3add6b33a9b1', None), 21),
    (('e78b02fe027621aec1227cbf5555c75775ba296b', None), 59),
], indirect=['repository_mining_cc_complex'])
def test_from_commit_with_merge_commit(repository_mining_cc_complex, expected_commits):
    assert len(repository_mining_cc_complex) == expected_commits


@pytest.mark.parametrize('repository_mining_cc_complex,expected_commits', [
    (('36287f7c3b09eff78395267a3ac0d7da067863fd', 'e78b02fe027621aec1227cbf5555c75775ba296b'), 5),
    (('70b71b7fd3c5973511904c468e464d4910597928', '90c0927162e4cef50fd65da6715932f908264d24'), 9),
    (('70b71b7fd3c5973511904c468e464d4910597928', 'c286db365e7374fe4d08f54077abb7fba81dd296'), 54),
    (('3bfbc107eac92f388de9f8b87682c3a0baf74981', 'c286db365e7374fe4d08f54077abb7fba81dd296'), 24),
], indirect=['repository_mining_cc_complex'])
def test_from_and_to_commit_with_merge_commit(repository_mining_cc_complex, expected_commits):
    assert len(repository_mining_cc_complex) == expected_commits


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
        for commit in Repository('test-repos/small_repo/',
                                 since=dt1,
                                 from_commit=from_commit
                                 ).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in Repository('test-repos/small_repo/',
                                 since=dt1,
                                 from_tag=from_tag).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in Repository('test-repos/small_repo/',
                                 from_commit=from_commit,
                                 from_tag=from_tag).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in Repository('test-repos/small_repo/',
                                 to=dt1,
                                 to_commit=from_commit
                                 ).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in Repository('test-repos/small_repo/',
                                 to=dt1,
                                 to_tag=from_tag).traverse_commits():
            print(commit.hash)

    with pytest.raises(Exception):
        for commit in Repository('test-repos/small_repo/',
                                 single=from_commit,
                                 to=dt1,
                                 to_tag=from_tag).traverse_commits():
            print(commit.hash)
