import pytest
from pydriller.metrics.process.owner_experience import OwnerExperience

test_data = [
   ('https://github.com/ishepard/pydriller', 'unexisting.java', None, '115953109b57d841ccd0952d70f8ed6703d175cd', (0, 0)),
   ('https://github.com/ishepard/pydriller', 'pydriller/repository_mining.py', None, '5a1a2b89c53a115e8087408469da04a7156ad808', (round(12/21, 4), round(23/10835, 4)))
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', test_data)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = OwnerExperience(path_to_repo=path_to_repo,
                                    filepath=filepath,
                                    from_commit=from_commit,
                                    to_commit=to_commit)
    count = metric.count()
    assert count == expected, f'Test failed because expected {str(expected)} and got {str(count)}!'
