import pytest
from pydriller.metrics.process.devs_count import DevsCount

test_data = [
   ('test-repos/git-1', 'unexisting.java', None, 'ffccf1e7497eb8136fd66ed5e42bef29677c4b71', (0, 0)),
   ('test-repos/git-1', 'Matricula.java',  None, 'ffccf1e7497eb8136fd66ed5e42bef29677c4b71', (1, 1)),
   ('https://github.com/ishepard/pydriller', 'domain/developer.py', None, '115953109b57d841ccd0952d70f8ed6703d175cd', (1, 0))
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', test_data)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = DevsCount(path_to_repo=path_to_repo,
                                    filepath=filepath,
                                    from_commit=from_commit,
                                    to_commit=to_commit)
    
    count = metric.count()
    assert count == expected, f'Test failed because expected {str(expected)} and got {str(count)}!'
