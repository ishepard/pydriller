import pytest
from datetime import datetime
from pydriller.metrics.process.change_set import ChangeSet

TEST_COMMIT_DATA = [
    ('test-repos/pydriller', 'ab36bf45859a210b0eae14e17683f31d19eea041', '71e053f61fc5d31b3e31eccd9c79df27c31279bf', 13, 8)
]


@pytest.mark.parametrize('path_to_repo, from_commit, to_commit, expected_max, expected_avg', TEST_COMMIT_DATA)
def test_with_commits(path_to_repo, from_commit, to_commit, expected_max, expected_avg):
    metric = ChangeSet(path_to_repo=path_to_repo,
                       from_commit=from_commit,
                       to_commit=to_commit)

    actual_max = metric.max()
    actual_avg = metric.avg()

    assert actual_max == expected_max
    assert actual_avg == expected_avg


TEST_DATE_DATA = [
    ('test-repos/pydriller', datetime(2018, 3, 21), datetime(2018, 3, 27), 13, 8),
    ('test-repos/pydriller', datetime(2018, 3, 23), datetime(2018, 3, 23), 0, 0)
]


@pytest.mark.parametrize('path_to_repo, since, to, expected_max, expected_avg', TEST_DATE_DATA)
def test_with_dates(path_to_repo, since, to, expected_max, expected_avg):
    metric = ChangeSet(path_to_repo=path_to_repo,
                       since=since,
                       to=to)

    actual_max = metric.max()
    actual_avg = metric.avg()

    assert actual_max == expected_max
    assert actual_avg == expected_avg
