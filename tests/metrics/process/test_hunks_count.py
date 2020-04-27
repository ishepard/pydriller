from pathlib import Path
from datetime import datetime

import pytest

from pydriller.metrics.process.hunks_count import HunksCount

TEST_COMMIT_DATA = [
    ('test-repos/pydriller', 'scm/git_repository.py', '71e053f61fc5d31b3e31eccd9c79df27c31279bf', '71e053f61fc5d31b3e31eccd9c79df27c31279bf', 8),
    ('test-repos/pydriller', 'scm/git_repository.py', 'ab36bf45859a210b0eae14e17683f31d19eea041', '71e053f61fc5d31b3e31eccd9c79df27c31279bf', 3),
    ('test-repos/pydriller', 'domain/modification.py', 'ab36bf45859a210b0eae14e17683f31d19eea041', 'fdf671856b260aca058e6595a96a7a0fba05454b', 1)
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_COMMIT_DATA)
def test_with_commits(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = HunksCount(path_to_repo=path_to_repo,
                        from_commit=from_commit,
                        to_commit=to_commit)

    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected

TEST_DATE_DATA = [
    ('test-repos/pydriller', 'scm/git_repository.py', datetime(2018, 3, 26), datetime(2018, 3, 27), 8),
    ('test-repos/pydriller', 'scm/git_repository.py', datetime(2018, 3, 21), datetime(2018, 3, 27), 3),
    ('test-repos/pydriller', 'domain/modification.py', datetime(2018, 3, 21), datetime(2018, 3, 22, 23), 1)
]

@pytest.mark.parametrize('path_to_repo, filepath, since, to, expected', TEST_DATE_DATA)
def test_with_dates(path_to_repo, filepath, since, to, expected):
    metric = HunksCount(path_to_repo=path_to_repo,
                        since=since,
                        to=to)

    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected