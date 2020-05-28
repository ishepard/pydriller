from pathlib import Path
from datetime import datetime

import pytest

from pydriller.metrics.process.contributors_experience import \
    ContributorsExperience

TEST_COMMIT_DATA = [
   ('test-repos/pydriller',
    'domain/modification.py',
    'fdf671856b260aca058e6595a96a7a0fba05454b',
    'ab36bf45859a210b0eae14e17683f31d19eea041',
    100.0),
   ('test-repos/pydriller',
    'pydriller/git_repository.py',
    'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5',
    'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5',
    100.0),
   ('test-repos/pydriller',
    'pydriller/git_repository.py',
    'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5',
    '9d0924301e4fae00eea6d00945bf834455e9a2a6',
    round(100*28/30, 2))
]


@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_COMMIT_DATA)
def test_with_commits(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = ContributorsExperience(path_to_repo=path_to_repo,
                                    from_commit=from_commit,
                                    to_commit=to_commit)
    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected


TEST_DATE_DATA = [
   ('test-repos/pydriller', 'domain/modification.py', datetime(2018, 3, 21), datetime(2018, 3, 23), 100.0),
   ('test-repos/pydriller', 'pydriller/git_repository.py', datetime(2018, 8, 1), datetime(2018, 8, 2), 100.0),
   ('test-repos/pydriller', 'pydriller/git_repository.py',  datetime(2018, 7, 23), datetime(2018, 8, 2), round(100*28/30, 2))
]


@pytest.mark.parametrize('path_to_repo, filepath, since, to, expected', TEST_DATE_DATA)
def test_with_dates(path_to_repo, filepath, since, to, expected):
    metric = ContributorsExperience(path_to_repo=path_to_repo,
                                    since=since,
                                    to=to)
    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected
