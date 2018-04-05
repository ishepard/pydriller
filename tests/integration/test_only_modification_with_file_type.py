import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

from pydriller.repository_mining import RepositoryMining


def test_mod_with_file_types():

    lc = list(RepositoryMining('test-repos/git-7/', only_modifications_with_file_types=['.java']).traverse_commits())

    assert 2 == len(lc)
    assert '5adbb71167e79ab6b974827e74c9da4d81977655' == lc[0].hash
    assert '0577bec2387ee131e1ccf336adcc172224d3f6f9' == lc[1].hash