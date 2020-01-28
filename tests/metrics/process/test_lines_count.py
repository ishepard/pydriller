import pytest
from pydriller.metrics.process.lines_count import NormalizedLinesCount

TEST_DATA = [
   ('https://github.com/ishepard/pydriller', '.gitignore', None, 'ab36bf45859a210b0eae14e17683f31d19eea041', {'added': 100, 'removed': 0}),
   ('https://github.com/ishepard/pydriller', '.gitignore', 'ab36bf45859a210b0eae14e17683f31d19eea041', 'ab36bf45859a210b0eae14e17683f31d19eea041', {'added': 100, 'removed': 0}),
   ('https://github.com/ishepard/pydriller', 'domain/modification.py', None, 'fdf671856b260aca058e6595a96a7a0fba05454b', {'added': round(100*1/49, 2), 'removed': 100}),
   ('https://github.com/ishepard/pydriller', 'domain/modification.py', 'ab36bf45859a210b0eae14e17683f31d19eea041', 'fdf671856b260aca058e6595a96a7a0fba05454b', {'added': round(100*1/49, 2), 'removed': 100})
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_DATA)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = NormalizedLinesCount(path_to_repo=path_to_repo,
                                  from_commit=from_commit,
                                  to_commit=to_commit)

    count = metric.count()
    assert count[filepath] == expected
