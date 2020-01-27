import pytest
from pydriller.metrics.process.devs_count import DevsCount

TEST_DATA = [
   ('https://github.com/ishepard/pydriller', 'pydriller/metrics/process/metrics.py', '115953109b57d841ccd0952d70f8ed6703d175cd', '8b69cae085581256adfdbd58c0e499395819b84d', 0),
   ('https://github.com/ishepard/pydriller', 'pydriller/git_repository.py', '115953109b57d841ccd0952d70f8ed6703d175cd', '8b69cae085581256adfdbd58c0e499395819b84d', 2)
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_DATA)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = DevsCount(path_to_repo=path_to_repo,
                       from_commit=from_commit,
                       to_commit=to_commit)
    
    count = metric.count()
    assert count.get(filepath, 0) == expected
