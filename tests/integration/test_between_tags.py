import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

from pydriller.repository_mining import RepositoryMining


def test_between_revisions():
    from_tag = 'tag1'
    to_tag = 'tag3'

    lc = list(RepositoryMining('test-repos/git-8/', from_tag=from_tag, to_tag=to_tag).traverse_commits())

    assert 5 == len(lc)
    assert '6bb9e2c6a8080e6b5b34e6e316c894b2ddbf7fcd' == lc[0].hash
    assert 'f1a90b8d7b151ceefd3e3dfc0dc1d0e12b5f48d0' == lc[1].hash
    assert '4638730126d40716e230c2040751a13153fb1556' == lc[2].hash
    assert 'a26f1438bd85d6b22497c0e5dae003812becd0bc' == lc[3].hash
    assert '627e1ad917a188a861c9fedf6e5858b79edbe439' == lc[4].hash
