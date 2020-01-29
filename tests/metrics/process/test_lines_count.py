import pytest

from pathlib import Path
from pydriller.metrics.process.lines_count import LinesCount

TEST_DATA = [
   ('https://github.com/ishepard/pydriller', '.gitignore', None, 'ab36bf45859a210b0eae14e17683f31d19eea041',
      {'added': 197, 'removed': 0, 'norm_added': 100.0, 'norm_removed': .0, 'total_added': 197, 'total_removed': 0}),

   ('https://github.com/ishepard/pydriller', '.gitignore', 'ab36bf45859a210b0eae14e17683f31d19eea041', 'ab36bf45859a210b0eae14e17683f31d19eea041',
      {'added': 197, 'removed': 0, 'norm_added': 100.0, 'norm_removed': .0, 'total_added': 197, 'total_removed': 0}),

   ('https://github.com/ishepard/pydriller', 'domain/modification.py', None, 'fdf671856b260aca058e6595a96a7a0fba05454b',
      {'added': 1, 'removed': 1, 'norm_added': round(100*1/49, 2), 'norm_removed': 100.0, 'total_added': 49, 'total_removed': 1}),

   ('https://github.com/ishepard/pydriller', 'domain/modification.py', 'ab36bf45859a210b0eae14e17683f31d19eea041', 'fdf671856b260aca058e6595a96a7a0fba05454b',
      {'added': 1, 'removed': 1, 'norm_added': round(100*1/49, 2), 'norm_removed': 100.0, 'total_added': 49, 'total_removed': 1})
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_DATA)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = LinesCount(path_to_repo=path_to_repo,
                        from_commit=from_commit,
                        to_commit=to_commit)

    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected
