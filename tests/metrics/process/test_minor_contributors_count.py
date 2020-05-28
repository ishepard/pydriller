from pathlib import Path
from datetime import datetime

import pytest

from pydriller.metrics.process.contributors_count import ContributorsCount

TEST_COMMIT_DATA = [
   ('test-repos/pydriller', 'pydriller/git_repository.py', 'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5', 'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5', 0),
   ('test-repos/pydriller', 'pydriller/git_repository.py', 'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5', 'ab36bf45859a210b0eae14e17683f31d19eea041', 1),
   ('test-repos/pydriller', 'pydriller/git_repository.py', '4af3839eb5ea5969f42142529a7a5526739fa570', 'ab36bf45859a210b0eae14e17683f31d19eea041', 2)
]


@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_COMMIT_DATA)
def test_with_commits(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = ContributorsCount(path_to_repo=path_to_repo,
                               from_commit=from_commit,
                               to_commit=to_commit)

    count = metric.count_minor()
    filepath = str(Path(filepath))
    assert count[filepath] == expected


TEST_DATE_DATA = [
   ('test-repos/pydriller', 'pydriller/git_repository.py', datetime(2018, 8, 1), datetime(2018, 8, 2), 0),
   ('test-repos/pydriller', 'pydriller/git_repository.py', datetime(2018, 3, 21), datetime(2018, 8, 2), 1),
   ('test-repos/pydriller', 'pydriller/git_repository.py', datetime(2018, 3, 21), datetime(2019, 1, 14, 10), 2)
]


@pytest.mark.parametrize('path_to_repo, filepath, since, to, expected', TEST_DATE_DATA)
def test_with_dates(path_to_repo, filepath, since, to, expected):
    metric = ContributorsCount(path_to_repo=path_to_repo,
                               since=since,
                               to=to)

    count = metric.count_minor()
    filepath = str(Path(filepath))
    assert count[filepath] == expected
