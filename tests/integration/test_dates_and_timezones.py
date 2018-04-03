import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

from typing import List

import pytest
from dateutil import tz

from domain.commit import Commit
from repository_mining import RepositoryMining
from tests.visitor_test import VisitorTest

from datetime import datetime
path2 = 'test-repos/git-2/'
path4 = 'test-repos/git-4/'


@pytest.yield_fixture(scope="function")
def lc(request):
    path, single = request.param
    mv = VisitorTest()
    RepositoryMining(path, mv, single=single).mine()
    yield mv.list_commits


@pytest.mark.parametrize('lc', [(path2, '29e929fbc5dc6a2e9c620069b24e2a143af4285f')], indirect=True)
def test_one_timezone(lc: List[Commit]):
    to_zone = tz.gettz('GMT+2')
    dt = datetime(2016, 4, 4, 13, 21, 25, tzinfo=to_zone)

    assert dt == lc[0].author_date


@pytest.mark.parametrize('lc', [(path4, '375de7a8275ecdc0b28dc8de2568f47241f443e9')], indirect=True)
def test_between_dates_reversed(lc: List[Commit]):
    to_zone = tz.gettz('GMT-4')
    dt = datetime(2016, 10, 8, 17, 57, 49, tzinfo=to_zone)

    assert dt == lc[0].author_date
