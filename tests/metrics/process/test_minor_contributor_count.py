import pytest
from pydriller.metrics.process.minor_contributor_count import MinorContributorCount

test_data = [
   ('https://github.com/ishepard/pydriller', 'unexisting.java', None, '115953109b57d841ccd0952d70f8ed6703d175cd', 0),
   ('https://github.com/PyGithub/PyGithub', 'github/Issue.py', None, 'd938f80be03878e0315409f8b4d0403d981d737f', 1)
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, expected', test_data)
def test(path_to_repo, filepath, from_commit, to_commit, expected):
    metric = MinorContributorCount(path_to_repo=path_to_repo,
                                    filepath=filepath,
                                    from_commit=from_commit,
                                    to_commit=to_commit)
    count = metric.count()
    assert count == expected, f'Test failed because expected {str(expected)} and got {str(count)}!'
