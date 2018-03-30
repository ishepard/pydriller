import pytest

from domain.commit import Commit
from scm.git_repository import GitRepository


@pytest.yield_fixture(scope="module")
def resource():
    yield GitRepository('test-repos/git-1/')


def test_equal(resource):
    c1: Commit = resource.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2')
    c2: Commit = resource.get_commit(c1.parents[0])
    c3: Commit = resource.get_commit('a4ece0762e797d2e2dcbd471115108dd6e05ff58')

    assert c1.parents[0] == 'a4ece0762e797d2e2dcbd471115108dd6e05ff58'
    assert c2 == c3
    assert c1 != c3