from pydriller.git import Git
import pytest
import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


@pytest.fixture
def repo(request):
    gr = Git(request.param)
    yield gr
    gr.clear()


@pytest.mark.parametrize("repo", ["test-repos/complex_repo"], indirect=True)
def test_commit_dictset(repo: Git):
    c1 = repo.get_commit("e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2")
    c2 = repo.get_commit(c1.parents[0])
    c3 = repo.get_commit("a4ece0762e797d2e2dcbd471115108dd6e05ff58")

    commit_dict = {c1: c1.hash, c2: c2.hash, c3: c3.hash}

    assert type(commit_dict) == dict
    assert commit_dict[c1] == "e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2"
    assert commit_dict[c2] == c1.parents[0]
    assert commit_dict[c3] == "a4ece0762e797d2e2dcbd471115108dd6e05ff58"
    assert commit_dict[c1] != commit_dict[c2]

    commit_set = {c1, c2, c3}
    assert type(commit_set) == set
    assert c1 in commit_set
    assert commit_set - {c1} == {c2, c3}


@pytest.mark.parametrize("repo", ["test-repos/complex_repo"], indirect=True)
def test_modification_dictset(repo: Git):
    c1 = repo.get_commit("e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2")
    c2 = repo.get_commit(c1.parents[0])

    m1 = c1.modified_files[0]
    m2s = c2.modified_files

    mod_dict = {m1: c1, m2s[0]: c2, m2s[1]: c2}

    assert type(mod_dict) == dict
    assert mod_dict[m1].hash == "e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2"
    assert mod_dict[m2s[0]].hash == c1.parents[0]
    assert mod_dict[m2s[1]].hash == c1.parents[0]
    assert m1 != m2s[0]

    mod_set = {m1}.union(set(m2s))
    assert type(mod_set) == set
    assert m1 in mod_set
    assert mod_set - {m1} == set(m2s)
