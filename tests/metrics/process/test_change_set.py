import pytest
from pydriller.metrics.process.change_set import ChangeSet

TEST_DATA = [
    ('test-repos/pydriller', 'ab36bf45859a210b0eae14e17683f31d19eea041', '71e053f61fc5d31b3e31eccd9c79df27c31279bf', 13, 8)
]

@pytest.mark.parametrize('path_to_repo, from_commit, to_commit, expected_max, expected_avg', TEST_DATA)
def test(path_to_repo, from_commit, to_commit, expected_max, expected_avg):
    metric = ChangeSet(path_to_repo=path_to_repo,
                       from_commit=from_commit,
                       to_commit=to_commit)

    actual_max = metric.max()
    actual_avg = metric.avg()

    assert actual_max == expected_max
    assert actual_avg == expected_avg
