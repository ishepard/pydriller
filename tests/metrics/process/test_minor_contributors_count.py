from pathlib import Path

import pytest

from pydriller.metrics.process.contributors_count import ContributorsCount

TEST_DATA = [
   ('test-repos/pydriller', 'pydriller/git_repository.py', 'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5', 'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5', 0),
   ('test-repos/pydriller', 'pydriller/git_repository.py', 'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5', 'ab36bf45859a210b0eae14e17683f31d19eea041', 1),
   ('test-repos/pydriller', 'pydriller/git_repository.py', '4af3839eb5ea5969f42142529a7a5526739fa570', 'ab36bf45859a210b0eae14e17683f31d19eea041', 2)
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_DATA)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = ContributorsCount(path_to_repo=path_to_repo,
                               from_commit=from_commit,
                               to_commit=to_commit)
    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath]['minor_contributors_count'] == expected
