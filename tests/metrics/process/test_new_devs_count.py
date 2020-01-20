import pytest
from pydriller.metrics.process.new_devs_count import NewDevsCount

test_data = [
   ('https://github.com/ishepard/pydriller', 'README.md', '9a0363f5b0300343ee1efedca0643c71120aba80', 0),
   ('https://github.com/ishepard/pydriller', 'README.md', '424617854e48fe7138c0d58e51c196b99024f774', 1),
   ('https://github.com/ishepard/pydriller', 'domain/developer.py', '424617854e48fe7138c0d58e51c196b99024f774', 1)
]

@pytest.mark.parametrize('path_to_repo, filepath, to_commit, expected', test_data)
def test(path_to_repo, filepath, to_commit, expected):
    metric = NewDevsCount(path_to_repo=path_to_repo,
                          filepath=filepath,
                          to_commit=to_commit)

    count = metric.count()
    assert count == expected, f'Test failed because expected {str(expected)} and got {str(count)}!'
