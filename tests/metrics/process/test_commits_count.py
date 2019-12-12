from pydriller.metrics.process.process_metrics import ProcessMetrics

def test_zero_commits_count_from_hash():
    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1',
                                           filepath='Arquivo.java',
                                           to_commit='ffccf1e7497eb8136fd66ed5e42bef29677c4b71')
    assert count == 0

def test_two_commits_count_from_hash():
    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Matricula.java', to_commit='ffccf1e7497eb8136fd66ed5e42bef29677c4b71')
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
    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Secao.java')
    assert count == 3

    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Secao.java', to_commit='f0dd1308bd904a9b108a6a40865166ee962af3d4')
    assert count == 3

    count = ProcessMetrics().commits_count(path_to_repo='test-repos/git-1', filepath='Secao.java', to_commit='71535a31f0b598a5d5fcebda7146ebc01def783a')
    assert count == 2

def test_from_latest_remote():
    count = ProcessMetrics().commits_count(path_to_repo='https://github.com/ishepard/pydriller', filepath='domain/developer.py', to_commit='fdf671856b260aca058e6595a96a7a0fba05454b')
    assert count == 2