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
    assert count == 6

def test_commits_count_with_renaming():
    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Matricula.javax')
    assert count == 6

    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Secao.javax')
    assert count == 3

def test_commits_count_til_creation_file():
    for commit in RepositoryMining('test-repos/git-1', reversed_order=True).traverse_commits():
        for m in commit.modifications:
            print(m.filename)
            print(m.change_type)
            print(m.old_path)

    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Secao.java')
    assert count == 3

    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Secao.java', commit_hash='f0dd1308bd904a9b108a6a40865166ee962af3d4')
    assert count == 3

    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Secao.java', commit_hash='71535a31f0b598a5d5fcebda7146ebc01def783a')
    assert count == 2
