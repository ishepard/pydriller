from pathlib import Path
from datetime import datetime

import pytest

from pydriller.metrics.process.contributors_count import ContributorsCount

TEST_COMMIT_DATA = [
   ('test-repos/pydriller', 'pydriller/git_repository.py', '8b69cae085581256adfdbd58c0e499395819b84d', '115953109b57d841ccd0952d70f8ed6703d175cd', 2),
   ('test-repos/pydriller', 'domain/modification.py', '71e053f61fc5d31b3e31eccd9c79df27c31279bf', 'ab36bf45859a210b0eae14e17683f31d19eea041', 1)
]


@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_COMMIT_DATA)
def test_with_commits(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = ContributorsCount(path_to_repo=path_to_repo,
                               from_commit=from_commit,
                               to_commit=to_commit)

    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected


TEST_DATE_DATA = [
   ('test-repos/pydriller', 'pydriller/git_repository.py', datetime(2019, 12, 17), datetime(2019, 12, 24), 2),
   ('test-repos/pydriller', 'domain/modification.py', datetime(2018, 3, 21), datetime(2018, 3, 27), 1)
]


@pytest.mark.parametrize('path_to_repo, filepath, since, to, expected', TEST_DATE_DATA)
def test_with_dates(path_to_repo, filepath, since, to, expected):
    metric = ContributorsCount(path_to_repo=path_to_repo,
                               since=since,
                               to=to)

    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected
