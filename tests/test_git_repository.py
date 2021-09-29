# Copyright 2018 Davide Spadini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest
from git import Git as PyGit

from pydriller.domain.commit import ModificationType
from pydriller.git import Git


@pytest.fixture
def repo(request):
    gr = Git(request.param)
    yield gr
    gr.clear()


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_projectname(repo: Git):
    assert repo.project_name == "small_repo"


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_get_head(repo: Git):
    assert repo is not None
    cs = repo.get_head()
    assert cs is not None

    assert cs.hash == 'da39b1326dbc2edfe518b90672734a08f3c13458'
    assert cs.author_date.timestamp() == 1522164679


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_list_commits(repo: Git):
    change_sets = list(repo.get_list_commits())

    list_commits = {'a88c84ddf42066611e76e6cb690144e5357d132c',
                    '6411e3096dd2070438a17b225f44475136e54e3a',
                    '09f6182cef737db02a085e1d018963c7a29bde5a',
                    '1f99848edadfffa903b8ba1286a935f1b92b2845',
                    'da39b1326dbc2edfe518b90672734a08f3c13458'}

    for commit in change_sets:
        assert commit.hash in list_commits

    assert len(change_sets) == 5


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_get_commit(repo: Git):
    c = repo.get_commit('09f6182cef737db02a085e1d018963c7a29bde5a')
    to_zone = timezone(timedelta(hours=1))

    assert c.hash == '09f6182cef737db02a085e1d018963c7a29bde5a'
    assert c.author.name == 'ishepard'
    assert c.committer.name == 'ishepard'
    assert c.author_date.timestamp() == datetime(2018, 3, 22, 10, 42, 3,
                                                 tzinfo=to_zone).timestamp()
    assert len(c.modified_files) == 1
    assert c.msg == 'Ooops file2'
    assert c.in_main_branch is True
    assert c.insertions == 4
    assert c.deletions == 0
    assert c.lines == 4
    assert c.files == 1


@pytest.mark.parametrize('repo', ['test-repos/detached_head/'], indirect=True)
def test_detached_head(repo: Git):
    c = repo.get_commit('56c5ef54d9d16d2b2255412f9479830b5b97cb99')
    assert c.in_main_branch is False


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_get_first_commit(repo: Git):
    c = repo.get_commit('a88c84ddf42066611e76e6cb690144e5357d132c')
    to_zone = timezone(timedelta(hours=1))

    assert c.hash == 'a88c84ddf42066611e76e6cb690144e5357d132c'
    assert c.author.name == 'ishepard'
    assert c.committer.name == 'ishepard'
    assert c.author_date.timestamp() == datetime(2018, 3, 22, 10, 41, 11,
                                                 tzinfo=to_zone).timestamp()
    assert c.committer_date.timestamp() == datetime(2018, 3, 22, 10, 41, 11,
                                                    tzinfo=to_zone).timestamp()
    assert len(c.modified_files) == 2
    assert c.msg == 'First commit adding 2 files'
    assert c.in_main_branch is True

    assert c.modified_files[0].change_type == ModificationType.ADD
    assert c.modified_files[1].change_type == ModificationType.ADD


@pytest.mark.parametrize('repo', ['test-repos/files/'], indirect=True)
def test_files(repo: Git):
    files = repo.files()
    assert len(files) == 8

    expected_files = (str(Path('test-repos/files/tmp1.py')),
                      str(Path('test-repos/files/tmp2.py')),
                      str(Path('test-repos/files/fold1/tmp3.py')),
                      str(Path('test-repos/files/fold1/tmp4.py')),
                      str(Path('test-repos/files/fold2/tmp5.py')),
                      str(Path('test-repos/files/fold2/tmp6.py')),
                      str(Path('test-repos/files/fold2/fold3/tmp7.py')),
                      str(Path('test-repos/files/fold2/fold3/tmp8.py')),
                      )
    for file in files:
        assert file.endswith(expected_files)


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_total_commits(repo: Git):
    assert repo.total_commits() == 5


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_get_commit_from_tag(repo: Git):
    commit = repo.get_commit_from_tag('v1.4')

    assert commit.hash == '09f6182cef737db02a085e1d018963c7a29bde5a'
    with pytest.raises(IndexError):
        repo.get_commit_from_tag('v1.5')


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_list_files_in_commit(repo: Git):
    repo.checkout('a7053a4dcd627f5f4f213dc9aa002eb1caf926f8')
    files1 = repo.files()
    assert len(files1) == 3
    repo.reset()

    repo.checkout('f0dd1308bd904a9b108a6a40865166ee962af3d4')
    files2 = repo.files()
    assert len(files2) == 2
    repo.reset()

    repo.checkout('9e71dd5726d775fb4a5f08506a539216e878adbb')
    files3 = repo.files()
    assert len(files3) == 3
    repo.reset()


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_checkout_consecutive_commits(repo: Git):
    repo.checkout('a7053a4dcd627f5f4f213dc9aa002eb1caf926f8')
    repo.checkout('f0dd1308bd904a9b108a6a40865166ee962af3d4')
    repo.checkout('9e71dd5726d775fb4a5f08506a539216e878adbb')
    files3 = repo.files()
    assert len(files3) == 3
    repo.reset()


@pytest.mark.parametrize('repo', ['test-repos/branches_without_files'], indirect=True)
def test_checkout_with_commit_not_fully_merged_to_master(repo: Git):
    repo.checkout('developing')
    files1 = repo.files()
    assert len(files1) == 2

    repo.reset()
    files2 = repo.files()
    assert len(files2) == 1

    repo.checkout('developing')
    files1 = repo.files()
    assert len(files1) == 2
    repo.reset()


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_get_all_commits(repo: Git):
    change_sets = list(repo.get_list_commits())

    assert len(change_sets) == 13
    assert change_sets[0].hash == '866e997a9e44cb4ddd9e00efe49361420aff2559'
    assert change_sets[12].hash == 'e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2'


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_branches_from_commit(repo: Git):
    commit = repo.get_commit('a997e9d400f742003dea601bb05a9315d14d1124')

    assert len(commit.branches) == 1
    assert 'b2' in commit.branches

    commit = repo.get_commit('866e997a9e44cb4ddd9e00efe49361420aff2559')
    assert len(commit.branches) == 2
    assert 'master' in commit.branches
    assert 'b2' in commit.branches


@pytest.mark.parametrize('repo', ['test-repos/branches_not_merged'], indirect=True)
def test_other_branches_with_merge(repo: Git):
    commit = repo.get_commit('7203c0b8220dcc7a59614bc7549799cd203ac072')
    assert commit.in_main_branch is False

    commit = repo.get_commit('87a31153090808f1e6f679a14ea28729a0b74f4d')
    assert commit.in_main_branch is False

    commit = repo.get_commit('b197ef4f0b4bc5b7d55c8949ecb1c861731f0b9d')
    assert commit.in_main_branch is True

    commit = repo.get_commit('e51421e0beae6a3c20bdcdfc21066e05db675e03')
    assert commit.in_main_branch is True


@pytest.mark.parametrize('repo', ['test-repos/branches_merged'], indirect=True)
def test_commit_in_master_branch(repo: Git):
    assert repo.get_head().hash == '29e929fbc5dc6a2e9c620069b24e2a143af4285f'

    repo.checkout('8986af2a679759e5a15794f6d56e6d46c3f302f1')

    git_to_change_head = Git('test-repos/branches_merged')
    commit = git_to_change_head.get_commit('8169f76a3d7add54b4fc7bca7160d1f1eede6eda')
    assert commit.in_main_branch is False

    repo.reset()
    assert repo.get_head().hash == '29e929fbc5dc6a2e9c620069b24e2a143af4285f'


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_should_detail_a_commit(repo: Git):
    commit = repo.get_commit('866e997a9e44cb4ddd9e00efe49361420aff2559')

    assert commit.author.name == "Maurício Aniche"
    assert commit.author.email == "mauricioaniche@gmail.com"

    assert commit.msg == "Matricula adicionada"
    assert len(commit.modified_files) == 1

    assert commit.modified_files[0].new_path == "Matricula.java"
    assert commit.modified_files[0].diff.startswith("@@ -0,0 +1,62 @@\n+package model;") is True
    assert commit.modified_files[0].source_code.startswith("package model;") is True


@pytest.mark.parametrize('repo', ['test-repos/branches_merged'], indirect=True)
def test_merge_commits(repo: Git):
    commit = repo.get_commit("168b3aab057ed61a769acf336a4ef5e64f76c9fd")
    assert commit.merge is False

    commit = repo.get_commit("8169f76a3d7add54b4fc7bca7160d1f1eede6eda")
    assert commit.merge is False

    commit = repo.get_commit("29e929fbc5dc6a2e9c620069b24e2a143af4285f")
    assert commit.merge is True


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_number_of_modified_files(repo: Git):
    commit = repo.get_commit('866e997a9e44cb4ddd9e00efe49361420aff2559')
    assert commit.modified_files[0].added_lines == 62
    assert commit.modified_files[0].deleted_lines == 0

    commit = repo.get_commit('d11dd6734ff4e60cac3a7b58d9267f138c9e05c7')
    assert commit.modified_files[0].added_lines == 1
    assert commit.modified_files[0].deleted_lines == 1


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_modification_status(repo: Git):
    commit = repo.get_commit('866e997a9e44cb4ddd9e00efe49361420aff2559')
    assert commit.modified_files[0].change_type == ModificationType.ADD
    assert commit.modified_files[0].old_path is None

    commit = repo.get_commit('57dbd017d1a744b949e7ca0b1c1a3b3dd4c1cbc1')
    assert commit.modified_files[0].change_type == ModificationType.MODIFY
    assert commit.modified_files[0].new_path == commit.modified_files[0].old_path

    commit = repo.get_commit('ffccf1e7497eb8136fd66ed5e42bef29677c4b71')
    assert commit.modified_files[0].change_type == ModificationType.DELETE
    assert commit.modified_files[0].new_path is None


@pytest.mark.parametrize('repo', ['test-repos/two_modifications/'], indirect=True)
def test_diffs(repo: Git):
    commit = repo.get_commit('93b4b18673ca6fb5d563bbf930c45cd1198e979b')

    assert len(commit.modified_files) == 2

    for mod in commit.modified_files:
        if mod.filename == 'file4.java':
            assert mod.deleted_lines == 8
            assert mod.added_lines == 0

        if mod.filename == 'file2.java':
            assert mod.deleted_lines == 12
            assert mod.added_lines == 0


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_detail_rename(repo: Git):
    commit = repo.get_commit('f0dd1308bd904a9b108a6a40865166ee962af3d4')

    assert commit.author.name == "Maurício Aniche"
    assert commit.author.email == "mauricioaniche@gmail.com"

    assert commit.modified_files[0].new_path == "Matricula.javax"
    assert commit.modified_files[0].old_path == "Matricula.java"


@pytest.mark.parametrize('repo', ['test-repos/branches_merged'], indirect=True)
def test_parent_commits(repo: Git):
    merge_commit = repo.get_commit('29e929fbc5dc6a2e9c620069b24e2a143af4285f')
    assert len(merge_commit.parents) == 2
    assert '8986af2a679759e5a15794f6d56e6d46c3f302f1' in merge_commit.parents
    assert '8169f76a3d7add54b4fc7bca7160d1f1eede6eda' in merge_commit.parents

    normal_commit = repo.get_commit('8169f76a3d7add54b4fc7bca7160d1f1eede6eda')
    assert len(normal_commit.parents) == 1
    assert '168b3aab057ed61a769acf336a4ef5e64f76c9fd' in normal_commit.parents


@pytest.mark.parametrize('repo', ['test-repos/tags'], indirect=True)
def test_tags(repo: Git):
    commit = repo.get_commit_from_tag('tag1')
    assert commit.hash == '6bb9e2c6a8080e6b5b34e6e316c894b2ddbf7fcd'

    commit = repo.get_commit_from_tag('tag2')
    assert commit.hash == '4638730126d40716e230c2040751a13153fb1556'

    with pytest.raises(IndexError):
        repo.get_commit_from_tag('tag4')


@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_simple(repo: Git):
    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit('e6d3b38a9ef683e8184eac10a0471075c2808bbd'))

    assert len(buggy_commits) == 1
    assert '540c7f31c18664a38190fafb6721b5174ff4a166' in buggy_commits[
        'B.java']


@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_multiple(repo: Git):
    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit('9942ee9dcdd1103e5808d544a84e6bc8cade0e54'))

    assert len(buggy_commits) == 1
    assert '2eb905e5e7be414fd184d6b4f1571b142621f4de' in buggy_commits[
        'A.java']
    assert '20a40688521c1802569e60f9d55342c3bfdd772c' in buggy_commits[
        'A.java']
    assert '22505e97dca6f843549b3a484b3609be4e3acf17' in buggy_commits[
        'A.java']


@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_rename_and_fix(repo: Git):
    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit('4e287ab8e6dba110219404fb8a43993f3dda674c'))

    assert len(buggy_commits) == 1
    assert '06b9ff31cd3475d9fd9ef668cc0844ab169da726' in buggy_commits[
        'H.java']


@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_rename(repo: Git):
    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit('2f2d0dec7cd06de4c2ed11ed010727a54af8ebf8'))

    assert len(buggy_commits) == 1
    assert '00e61714fd76ff110d8da953aa1179809591f5aa' in buggy_commits[
        str(Path('myfolder/Z.java'))]


@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_useless_lines(repo: Git):
    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit('3bc7295c16b7dfc15d5f82eb6962a2774e1b8420'))
    assert len(buggy_commits) == 1
    assert 'c7fc2e870ce03b0b8dc29ed0eeb26d14e235ea3b' in buggy_commits[
        'H.java']


@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_useless_lines2(repo: Git):
    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit('4155c421ee5cbb3c34feee7b68aa78a2ee1bbeae'))
    assert len(buggy_commits) == 0


@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_for_single_file(repo: Git):
    commit = repo.get_commit('0f726924f96621e4965039123098ba83e39ffba6')
    buggy_commits = None
    for mod in commit.modified_files:
        if mod.filename == 'A.java':
            buggy_commits = repo.get_commits_last_modified_lines(commit, mod)

    assert buggy_commits
    assert len(buggy_commits) == 1
    assert 'e2ed043eb96c05ebde653a44ae733ded9ef90750' in buggy_commits['A.java']
    assert 1 == len(buggy_commits['A.java'])


@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_with_more_modification(repo: Git):
    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit('c7002fb321a8ba32a28fac200538f7c2ba76f175'))
    assert len(buggy_commits) == 1
    assert '5cb9e9ae44a0949ec91d06a955975289be766f34' in buggy_commits[
        'A.java']


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_get_commits_modified_file(repo: Git):
    commits = repo.get_commits_modified_file('file2.java')

    assert len(commits) == 3
    assert '09f6182cef737db02a085e1d018963c7a29bde5a' in commits
    assert '6411e3096dd2070438a17b225f44475136e54e3a' in commits
    assert 'a88c84ddf42066611e76e6cb690144e5357d132c' in commits


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_get_commits_modified_file_missing_file(repo: Git):
    commits = repo.get_commits_modified_file('non-existing-file.java')

    assert len(commits) == 0


@pytest.mark.parametrize('repo', ['test-repos/tags'], indirect=True)
def test_get_tagged_commits(repo: Git):
    tagged_commits = repo.get_tagged_commits()

    assert len(tagged_commits) == 3
    assert '6bb9e2c6a8080e6b5b34e6e316c894b2ddbf7fcd' == tagged_commits[0]
    assert '4638730126d40716e230c2040751a13153fb1556' == tagged_commits[1]
    assert '627e1ad917a188a861c9fedf6e5858b79edbe439' == tagged_commits[2]


@pytest.mark.parametrize('repo', ['test-repos/different_files'], indirect=True)
def test_get_tagged_commits_wo_tags(repo: Git):
    tagged_commits = repo.get_tagged_commits()

    assert len(tagged_commits) == 0


@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_hyper_blame(repo: Git):
    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit(
        'e6d3b38a9ef683e8184eac10a0471075c2808bbd'))

    assert len(buggy_commits) == 1
    assert '540c7f31c18664a38190fafb6721b5174ff4a166' in buggy_commits[
        'B.java']


@pytest.mark.skipif(PyGit().version_info < (2, 23),
                    reason="requires 2.23 or higher")
@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_hyper_blame_unblamable(tmp_path, repo: Git):
    p = tmp_path / "ignore.txt"
    p.write_text("540c7f31c18664a38190fafb6721b5174ff4a166")

    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit(
        'e6d3b38a9ef683e8184eac10a0471075c2808bbd'),
        hashes_to_ignore_path=str(p))

    assert len(buggy_commits) == 0


@pytest.mark.skipif(PyGit().version_info < (2, 23),
                    reason="requires git 2.23 or higher")
@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_hyper_blame_ignore_hash(tmp_path, repo: Git):
    p = tmp_path / "ignore.txt"
    p.write_text("5cb9e9ae44a0949ec91d06a955975289be766f34")

    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit(
        'c7002fb321a8ba32a28fac200538f7c2ba76f175'),
        hashes_to_ignore_path=str(p))

    assert len(buggy_commits) == 1
    assert 'c41d270f8abc203c895309235adbd5f3f81d4a45' in buggy_commits[
        'A.java']


@pytest.mark.parametrize('repo', ['test-repos/szz/'], indirect=True)
def test_get_commits_last_modified_lines_hyper_blame_with_renaming(repo: Git):
    buggy_commits = repo.get_commits_last_modified_lines(repo.get_commit(
        'be0772cbaa2eba32bf97aae885199d1a357ddc93'))

    assert len(buggy_commits) == 2
    assert '9568d20856728304ab0b4d2d02fb9e81d0e5156d' in buggy_commits[
        'A.java']
    assert '9568d20856728304ab0b4d2d02fb9e81d0e5156d' in buggy_commits[
        'H.java']
