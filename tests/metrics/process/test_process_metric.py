import pytest

from datetime import datetime
from pydriller.metrics.process.process_metric import ProcessMetric

dt1 = datetime(2016, 10, 8, 17, 0, 0)
dt2 = datetime(2016, 10, 8, 17, 59, 0)

TEST_DATA = [
    ('test-repos/pydriller', None, dt2, None, '81ddf7e78d92f3aaa212d5924d1ae0ed1fd980e6'),  # Test (if not since and not from_commit)
    ('test-repos/pydriller', dt1, None, 'ab36bf45859a210b0eae14e17683f31d19eea041', None)   # Test (if not to and not to_commit)
]


@pytest.mark.parametrize('path_to_repo, since, to, from_commit, to_commit', TEST_DATA)
def test_type_error(path_to_repo, since, to, from_commit, to_commit):

    with pytest.raises(TypeError):
        ProcessMetric(path_to_repo=path_to_repo,
                      since=since,
                      to=to,
                      from_commit=from_commit,
                      to_commit=to_commit)
