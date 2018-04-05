import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

import pytest

from pydriller.repository_mining import RepositoryMining


@pytest.yield_fixture(scope="function")
def lc(request):
    reversed = request.param
    yield list(RepositoryMining('test-repos/git-4', reversed_order=reversed).traverse_commits())


@pytest.mark.parametrize('lc', [False], indirect=True)
def test_should_visit_ascendent_order(lc):
    assert 3 == len(lc)
    assert 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5' == lc[0].hash
    assert '375de7a8275ecdc0b28dc8de2568f47241f443e9' == lc[1].hash
    assert 'b8c2be250786975f1c6f47e96922096f1bb25e39' == lc[2].hash



@pytest.mark.parametrize('lc', [True], indirect=True)
def test_should_visit_descendent_order(lc):
    assert 3 == len(lc)
    assert 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5' == lc[2].hash
    assert '375de7a8275ecdc0b28dc8de2568f47241f443e9' == lc[1].hash
    assert 'b8c2be250786975f1c6f47e96922096f1bb25e39' == lc[0].hash