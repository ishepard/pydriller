import math, pytest
from pydriller.metrics.process.devs_experience import DevsExperience

test_data = [
   ('https://github.com/ishepard/pydriller', 'unexisting.java', None, '115953109b57d841ccd0952d70f8ed6703d175cd', (0, 0, 0)),
   ('https://github.com/ishepard/pydriller', 'pydriller/repository_mining.py', None, '5a1a2b89c53a115e8087408469da04a7156ad808', (round(12/573, 4), round(101/10835, 4), round(math.pow(5211000060, 1/5), 2)))
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', test_data)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = DevsExperience(path_to_repo=path_to_repo,
                                    filepath=filepath,
                                    from_commit=from_commit,
                                    to_commit=to_commit)
    count = metric.count()
    assert count == expected