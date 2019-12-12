from pydriller.metrics.process.process_metrics import ProcessMetrics

from pydriller.repository_mining import RepositoryMining

def test_zero_commits_count_from_hash():
    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Arquivo.java', commit_hash='ffccf1e7497eb8136fd66ed5e42bef29677c4b71')
    assert count == 0

def test_two_commits_count_from_hash():
    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Matricula.java', commit_hash='ffccf1e7497eb8136fd66ed5e42bef29677c4b71')
    assert count == 2

def test_zero_commits_count_from_latest():
    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='unexisting.java')
    assert count == 0
    
def test_from_latest():
    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Arquivo.java')
    assert count == 2

    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Matricula.java')
    assert count == 5
    
