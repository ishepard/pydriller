import pytest
from pydriller.metrics.process.lines_count import NormalizedLinesCount

test_data = [
   ('https://github.com/ishepard/pydriller', 'README.md', None, '772c636bb098eaba6adbafe301ce69d5f25c2c7a', (0, 0)),
   ('https://github.com/ishepard/pydriller', 'README.md', None, 'bf5208c06e64153d180faf26cd9a86426631c2e4', (float(15/246), float(7/24))),
   ('https://github.com/ishepard/pydriller', 'README.md', None, 'e7255f596a1cde0f9f42a962969d541e5186c441', (1, 0))
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', test_data)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = NormalizedLinesCount(path_to_repo=path_to_repo,
                                    filepath=filepath,
                                    from_commit=from_commit,
                                    to_commit=to_commit)
    
    count = metric.count()
    assert count == expected, f'Test failed because expected {str(expected)} and got {str(count)}!'
