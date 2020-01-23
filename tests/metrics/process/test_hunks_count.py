import pytest
from pydriller.metrics.process.hunks_count import HunksCount

test_data = [
    ('https://github.com/ishepard/pydriller', 'pydriller/repository_mining.py', None, '4be0402d466470ae7274c4244bad2712dfeda3ab', 2),
    ('https://github.com/ishepard/pydriller', 'README.md', None, 'e7255f596a1cde0f9f42a962969d541e5186c441', 1)
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', test_data)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = HunksCount(path_to_repo=path_to_repo,
                                    filepath=filepath,
                                    from_commit=from_commit,
                                    to_commit=to_commit)
    
    count = metric.count()
    assert count == expected
