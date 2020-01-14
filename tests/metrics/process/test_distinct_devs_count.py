from pydriller.metrics.process.process_metrics import ProcessMetrics

def test_distinct_devs_from_hash():
    count = ProcessMetrics().distinct_dev_count(
        path_to_repo='test-repos/git-1', filepath='unexisting.java',
        to_commit='ffccf1e7497eb8136fd66ed5e42bef29677c4b71')
    assert count == 0

    count = ProcessMetrics().distinct_dev_count(path_to_repo='test-repos/git-1', filepath='Matricula.java', to_commit='ffccf1e7497eb8136fd66ed5e42bef29677c4b71')
    assert count == 1

def test_distinct_devs_from_latest():
    count = ProcessMetrics().distinct_dev_count(path_to_repo='test-repos/git-1', filepath='unexisting.java')
    assert count == 0
    
    count = ProcessMetrics().distinct_dev_count(path_to_repo='test-repos/git-1', filepath='Arquivo.java')
    assert count == 1

    count = ProcessMetrics().distinct_dev_count(path_to_repo='test-repos/git-1', filepath='Matricula.java')
    assert count == 1

def test_distinct_devs_with_renaming():
    count = ProcessMetrics().distinct_dev_count(path_to_repo='test-repos/git-1', filepath='Matricula.javax')
    assert count == 1

    count = ProcessMetrics().distinct_dev_count(path_to_repo='test-repos/git-1', filepath='Secao.javax')
    assert count == 1

def test_distinct_devs_til_creation_file():
    count = ProcessMetrics().distinct_dev_count(path_to_repo='test-repos/git-1', filepath='Secao.java')
    assert count == 1

    count = ProcessMetrics().distinct_dev_count(path_to_repo='test-repos/git-1', filepath='Secao.java', to_commit='f0dd1308bd904a9b108a6a40865166ee962af3d4')
    assert count == 1

def test_distinct_devs_from_latest_remote():
    count = ProcessMetrics().distinct_dev_count(path_to_repo='https://github.com/ishepard/pydriller', filepath='domain/developer.py', to_commit='fdf671856b260aca058e6595a96a7a0fba05454b')
    assert count == 1

def test_distinct_devs_from_latest_remote2():
    count = ProcessMetrics().distinct_dev_count(path_to_repo='https://github.com/ishepard/pydriller', filepath='domain/developer.py')
    assert count == 1
