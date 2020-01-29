import pytest

from pathlib import Path
from pydriller.metrics.process.contributors_experience import ContributorsExperience

TEST_DATA = [
   ('https://github.com/ishepard/pydriller', 'domain/modification.py', None, 'fdf671856b260aca058e6595a96a7a0fba05454b', 100.0),
   ('https://github.com/ishepard/pydriller', 'pydriller/git_repository.py', 'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5', 'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5', 100.0),
   ('https://github.com/ishepard/pydriller', 'pydriller/git_repository.py', '9d0924301e4fae00eea6d00945bf834455e9a2a6', 'e9854bbea1cb7b7f06cbb559f7b06724d11ae1e5', round(100*28/30, 2))
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_DATA)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = ContributorsExperience(path_to_repo=path_to_repo,
                                    from_commit=from_commit,
                                    to_commit=to_commit)
    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected