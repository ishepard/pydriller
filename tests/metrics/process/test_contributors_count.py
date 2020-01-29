import pytest

from pathlib import Path
from pydriller.metrics.process.contributors_count import ContributorsCount

TEST_DATA = [
   ('https://github.com/ishepard/pydriller', 'pydriller/git_repository.py', '115953109b57d841ccd0952d70f8ed6703d175cd', '8b69cae085581256adfdbd58c0e499395819b84d', 2),
   ('https://github.com/ishepard/pydriller', 'domain/modification.py', None, '71e053f61fc5d31b3e31eccd9c79df27c31279bf', 1)
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_DATA)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = ContributorsCount(path_to_repo=path_to_repo,
                               from_commit=from_commit,
                               to_commit=to_commit)

    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath]['contributors_count'] == expected
