import pytest
from pathlib import Path
from pydriller.metrics.process.lines_count import LinesCount

TEST_DATA = [
   ('test-repos/pydriller', '.gitignore', 'ab36bf45859a210b0eae14e17683f31d19eea041', 'ab36bf45859a210b0eae14e17683f31d19eea041', 197),
   ('test-repos/pydriller', 'domain/modification.py', 'ab36bf45859a210b0eae14e17683f31d19eea041', '71e053f61fc5d31b3e31eccd9c79df27c31279bf', 65)
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected_count', TEST_DATA)
def test(path_to_repo, filepath, from_commit, to_commit, expected_count):
    metric = LinesCount(path_to_repo=path_to_repo,
                        from_commit=from_commit,
                        to_commit=to_commit)

    actual_count = metric.count()
    filepath = str(Path(filepath))

    assert actual_count[filepath] == expected_count
