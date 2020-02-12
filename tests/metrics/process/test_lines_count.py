from pathlib import Path

import pytest

from pydriller.metrics.process.lines_count import LinesCount

TEST_DATA = [
   ('test-repos/pydriller', '.gitignore', 'ab36bf45859a210b0eae14e17683f31d19eea041', 'ab36bf45859a210b0eae14e17683f31d19eea041',
      {'added': 197, 'removed': 0}),

   ('test-repos/pydriller', 'domain/modification.py', 'fdf671856b260aca058e6595a96a7a0fba05454b', 'ab36bf45859a210b0eae14e17683f31d19eea041',
      {'added': 49, 'removed': 1})
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_DATA)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = LinesCount(path_to_repo=path_to_repo,
                        from_commit=from_commit,
                        to_commit=to_commit)

    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected
