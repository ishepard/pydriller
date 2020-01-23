import pytest
from pydriller.metrics.process.commit_count import CommitCount

test_data = [
    ('test-repos/git-1', 'Arquivo.java', None, 'ffccf1e7497eb8136fd66ed5e42bef29677c4b71', False, 0),
    ('test-repos/git-1', 'Matricula.java', None, 'ffccf1e7497eb8136fd66ed5e42bef29677c4b71', False, 2),
    ('test-repos/git-1', 'unexisting.java', None, None, False, 0),
    ('test-repos/git-1', 'Matricula.java', None, None, False, 6),
    ('https://github.com/ishepard/pydriller', 'domain/developer.py', None, 'fdf671856b260aca058e6595a96a7a0fba05454b', False, 2),
    ('https://github.com/ishepard/pydriller', 'domain/developer.py', None, 'fdf671856b260aca058e6595a96a7a0fba05454b', True, 2)
]

@pytest.mark.parametrize('path_to_repo, filepath, from_commit, to_commit, release_scope, expected', test_data)
def test(path_to_repo, filepath, from_commit, to_commit, release_scope, expected):
    metric = CommitCount(path_to_repo=path_to_repo,
                                    filepath=filepath,
                                    from_commit=from_commit,
                                    to_commit=to_commit,
                                    release_scope=release_scope)
    
    count = metric.count()
    assert count == expected
