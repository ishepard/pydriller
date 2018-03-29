import pytest

from domain.commit import Commit
from repository_mining import RepositoryMining
from scm.commit_visitor import CommitVisitor
from scm.git_repository import GitRepository
from scm.persistence_mechanism import PersistenceMechanism
from datetime import datetime
from dateutil import tz
from tests.visitor_test import VisitorTest

to_zone = tz.gettz('GMT+1')
dt = datetime(2018, 3, 22, 10, 41, 30, tzinfo=to_zone)
dt1 = datetime(2018, 3, 22, 10, 42, 3, tzinfo=to_zone)
dt2 = datetime(2018, 3, 22, 10, 41, 45, tzinfo=to_zone)
to_zone = tz.gettz('GMT+2')
dt3 = datetime(2018, 3, 27, 17, 20, 3, tzinfo=to_zone)


@pytest.fixture(scope="function")
def lc_since_to(request):
    since, to = request.param
    mv = VisitorTest()
    RepositoryMining('test-repos/test1/', mv, since=since, to=to).mine()
    yield mv.list_commits
    print("teardown")


@pytest.fixture(scope="function")
def lc_from_to_commit(request):
    from_commit, to_commit = request.param
    mv = VisitorTest()
    RepositoryMining('test-repos/test1/', mv, from_commit=from_commit, to_commit=to_commit).mine()
    yield mv.list_commits
    print("teardown")


@pytest.fixture(scope="function")
def lc_from_to_tag(request):
    from_tag, to_tag= request.param
    mv = VisitorTest()
    RepositoryMining('test-repos/test1/', mv, from_tag=from_tag, to_tag=to_tag).mine()
    yield mv.list_commits
    print("teardown")


@pytest.mark.parametrize('lc_since_to', [(None, None)], indirect=True)
def test_no_filters(lc_since_to):
    assert 5 == len(lc_since_to)


@pytest.mark.parametrize('lc_since_to', [(dt, None)], indirect=True)
def test_since_filter(lc_since_to):
    assert 4 == len(lc_since_to)


@pytest.mark.parametrize('lc_since_to', [(None, dt1)], indirect=True)
def test_to_filter(lc_since_to):
    assert 3 == len(lc_since_to)


@pytest.mark.parametrize('lc_since_to', [(dt2, dt3)], indirect=True)
def test_since_and_to_filters(lc_since_to):
    assert 3 == len(lc_since_to)


@pytest.mark.parametrize('lc_from_to_commit', [('6411e3096dd2070438a17b225f44475136e54e3a', None)], indirect=True)
def test_from_commit_filter(lc_from_to_commit):
    assert 4 == len(lc_from_to_commit)


@pytest.mark.parametrize('lc_from_to_commit', [(None, '09f6182cef737db02a085e1d018963c7a29bde5a')], indirect=True)
def test_to_commit_filter(lc_from_to_commit):
    assert 3 == len(lc_from_to_commit)


@pytest.mark.parametrize('lc_from_to_commit', [('6411e3096dd2070438a17b225f44475136e54e3a', '09f6182cef737db02a085e1d018963c7a29bde5a')], indirect=True)
def test_from_and_to_commit_filters(lc_from_to_commit):
    assert 2 == len(lc_from_to_commit)


@pytest.mark.parametrize('lc_from_to_tag', [('v1.4', None)], indirect=True)
def test_from_tag_filter(lc_from_to_tag):
    assert 3 == len(lc_from_to_tag)


@pytest.mark.parametrize('lc_from_to_tag', [(None, 'v1.4')], indirect=True)
def test_from_tag_filter(lc_from_to_tag):
    assert 3 == len(lc_from_to_tag)


def test_multiple_filters_exceptions():
    mv = VisitorTest()
    from_commit = '6411e3096dd2070438a17b225f44475136e54e3a'
    from_tag = 'v1.4'

    with pytest.raises(Exception):
        RepositoryMining('test-repos/test1/', mv, from_commit=from_commit, from_tag=from_tag)

    with pytest.raises(Exception):
        RepositoryMining('test-repos/test1/', mv, since=dt2, from_commit=from_commit)

    with pytest.raises(Exception):
        RepositoryMining('test-repos/test1/', mv, since=dt2, from_tag=from_tag)

    with pytest.raises(Exception):
        RepositoryMining('test-repos/test1/', mv, to=dt2, to_tag=from_tag)