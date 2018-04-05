import logging
from datetime import datetime
from dateutil import tz
from pydriller.repository_mining import RepositoryMining
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


to_zone = tz.gettz('GMT-4')
dt1 = datetime(2016, 10, 8, 17, 0, 0, tzinfo=to_zone)
dt2 = datetime(2016, 10, 8, 17, 59, 0, tzinfo=to_zone)


def test_between_dates():
    list_commits = list(RepositoryMining('test-repos/git-4/', since=dt1, to=dt2).traverse_commits())

    assert 2 == len(list_commits)
    assert 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5' == list_commits[0].hash
    assert '375de7a8275ecdc0b28dc8de2568f47241f443e9' == list_commits[1].hash


def test_between_dates_reversed():
    # logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    lc = list(RepositoryMining('test-repos/git-4/', since=dt1, to=dt2, reversed_order=True).traverse_commits())

    assert 2 == len(lc)
    assert '375de7a8275ecdc0b28dc8de2568f47241f443e9' == lc[0].hash
    assert 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5' == lc[1].hash
