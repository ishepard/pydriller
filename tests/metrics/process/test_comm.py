from pydriller.metrics.process.comm import COMM

def test_zero_commits_count():
    count = COMM().count(path_to_repo='test-repos/git-1', commit_hash='ffccf1e7497eb8136fd66ed5e42bef29677c4b71', filename='Arquivo.java')
    assert count == 0

def test_two_commits_count():
    count = COMM().count(path_to_repo='test-repos/git-1', commit_hash='ffccf1e7497eb8136fd66ed5e42bef29677c4b71', filename='Matricula.java')
    assert count == 2
