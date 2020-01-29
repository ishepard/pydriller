import pytest

from pathlib import Path
from pydriller.metrics.process.history_complexity import HistoryComplexity

TEST_DATA = [
    ('https://github.com/ishepard/pydriller', 'scm/git_repository.py', '90ca34ebfe69629cb7f186a1582fc38a73cc572e', '90ca34ebfe69629cb7f186a1582fc38a73cc572e', 40.49),
    ('https://github.com/ishepard/pydriller', 'scm/git_repository.py', '90ca34ebfe69629cb7f186a1582fc38a73cc572e', '71e053f61fc5d31b3e31eccd9c79df27c31279bf', 47.05)
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', TEST_DATA)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = HistoryComplexity(path_to_repo=path_to_repo,
                               from_commit=from_commit,
                               to_commit=to_commit)
    
    count = metric.count()
    filepath = str(Path(filepath))
    assert count[filepath] == expected
