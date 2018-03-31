from repository_mining import RepositoryMining
from tests.visitor_test import VisitorTest


def test_mod_with_file_types():
    mv = VisitorTest()
    RepositoryMining('test-repos/git-7/', mv, only_modifications_with_file_types=['.java']).mine()
    lc = mv.list_commits

    assert 2 == len(lc)
    assert '5adbb71167e79ab6b974827e74c9da4d81977655' == lc[0].hash
    assert '0577bec2387ee131e1ccf336adcc172224d3f6f9' == lc[1].hash