import pytest

from pathlib import Path
from pydriller.metrics.process.metrics import history_complexity

TEST_DATA = [
    ('https://github.com/ishepard/pydriller', 'scm/git_repository.py',
        [('90ca34ebfe69629cb7f186a1582fc38a73cc572e', '90ca34ebfe69629cb7f186a1582fc38a73cc572e'),
        ('71e053f61fc5d31b3e31eccd9c79df27c31279bf', '71e053f61fc5d31b3e31eccd9c79df27c31279bf')],
        40.49+42.68)
]

@pytest.mark.parametrize('path_to_repo, filepath, periods, expected', TEST_DATA)
def test(path_to_repo, filepath, periods, expected):
    result = history_complexity(path_to_repo=path_to_repo, periods=periods)
    filepath = str(Path(filepath))
    assert result[filepath] == expected