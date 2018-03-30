from datetime import datetime
import pytest
from dateutil import tz

from repository_mining import RepositoryMining
from tests.visitor_test import VisitorTest


@pytest.yield_fixture(scope="function")
def lc(request):
    reversed = request.param
    to_zone = tz.gettz('GMT-4')
    dt1 = datetime(2016, 10, 8, 17, 0, 0, tzinfo=to_zone)
    dt2 = datetime(2016, 10, 8, 17, 59, 0, tzinfo=to_zone)
    mv = VisitorTest()
    RepositoryMining('test-repos/git-4/', mv, since=dt1, to=dt2, reversed_order=reversed).mine()
    yield mv.list_commits


@pytest.mark.parametrize('lc', [False], indirect=True)
def test_between_dates(lc):
    assert 2 == len(lc)
    assert 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5' == lc[0].hash
    assert '375de7a8275ecdc0b28dc8de2568f47241f443e9' == lc[1].hash


@pytest.mark.parametrize('lc', [True], indirect=True)
def test_between_dates_reversed(lc):
    assert 2 == len(lc)
    assert '375de7a8275ecdc0b28dc8de2568f47241f443e9' == lc[0].hash
    assert 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5' == lc[1].hash
