from pathlib import Path

import pytest

from pydriller.metrics.process.commits_count import CommitsCount

TEST_DATA = [
    ('test-repos/pydriller', 'domain/developer.py', 'fdf671856b260aca058e6595a96a7a0fba05454b', 'ab36bf45859a210b0eae14e17683f31d19eea041', 2),
    ('test-repos/pydriller', 'domain/developer.py', 'ab36bf45859a210b0eae14e17683f31d19eea041', 'fdf671856b260aca058e6595a96a7a0fba05454b', 2)
]


@pytest.mark.parametrize('path_to_repo, filepath, from_commit, '
                         'to_commit, expected', TEST_DATA)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = CommitsCount(path_to_repo=path_to_repo,
                          from_commit=from_commit,
                          to_commit=to_commit)
    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected
