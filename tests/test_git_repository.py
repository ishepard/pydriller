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

import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest

from pydriller.domain.commit import ModificationType
from pydriller.git_repository import GitRepository

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def test_projectname():
    gr = GitRepository('test-repos/test1/')
    assert gr.project_name == "test1"

    gr = GitRepository('test-repos/test1')
    assert gr.project_name == "test1"


def test_get_head():
    gr = GitRepository('test-repos/test1/')
    assert gr is not None
    cs = gr.get_head()
    assert cs is not None

    assert cs.hash == 'da39b1326dbc2edfe518b90672734a08f3c13458'
    assert 1522164679 == cs.author_date.timestamp()


def test_list_commits():
    gr = GitRepository('test-repos/test1/')
    assert gr is not None
    change_sets = list(gr.get_list_commits())

    list_commits = ['a88c84ddf42066611e76e6cb690144e5357d132c', '6411e3096dd2070438a17b225f44475136e54e3a',
                    '09f6182cef737db02a085e1d018963c7a29bde5a', '1f99848edadfffa903b8ba1286a935f1b92b2845',
                    'da39b1326dbc2edfe518b90672734a08f3c13458']

    for commit in change_sets:
        assert commit.hash in list_commits
    assert 5 == len(change_sets)


def test_get_commit():
    gr = GitRepository('test-repos/test1/')
    c = gr.get_commit('09f6182cef737db02a085e1d018963c7a29bde5a')
    to_zone = timezone(timedelta(hours=1))

    assert '09f6182cef737db02a085e1d018963c7a29bde5a' == c.hash
    assert 'ishepard' == c.author.name
    assert 'ishepard' == c.committer.name
    assert datetime(2018, 3, 22, 10, 42, 3, tzinfo=to_zone).timestamp() == c.author_date.timestamp()
    assert 1 == len(c.modifications)
    assert 'Ooops file2' == c.msg
    assert c.in_main_branch is True


def test_get_first_commit():
    gr = GitRepository('test-repos/test1/')
    c = gr.get_commit('a88c84ddf42066611e76e6cb690144e5357d132c')
    to_zone = timezone(timedelta(hours=1))

    assert 'a88c84ddf42066611e76e6cb690144e5357d132c' == c.hash
    assert 'ishepard' == c.author.name
    assert 'ishepard' == c.committer.name
    assert datetime(2018, 3, 22, 10, 41, 11, tzinfo=to_zone).timestamp() == c.author_date.timestamp()
    assert datetime(2018, 3, 22, 10, 41, 11, tzinfo=to_zone).timestamp() == c.committer_date.timestamp()
    assert 2 == len(c.modifications)
    assert 'First commit adding 2 files' == c.msg
    assert c.in_main_branch is True


def test_files():
    gr = GitRepository('test-repos/test2')
    all = gr.files()

    assert 8 == len(all)
    assert str(Path('test-repos/test2/tmp1.py')) in all
    assert str(Path('test-repos/test2/tmp2.py')) in all
    assert str(Path('test-repos/test2/fold1/tmp3.py')) in all
    assert str(Path('test-repos/test2/fold1/tmp4.py')) in all
    assert str(Path('test-repos/test2/fold2/tmp5.py')) in all
    assert str(Path('test-repos/test2/fold2/tmp6.py')) in all
    assert str(Path('test-repos/test2/fold2/fold3/tmp7.py')) in all
    assert str(Path('test-repos/test2/fold2/fold3/tmp8.py')) in all


def test_total_commits():
    gr = GitRepository('test-repos/test1/')
    assert 5 == gr.total_commits()


def test_get_commit_from_tag():
    gr = GitRepository('test-repos/test1/')

    commit = gr.get_commit_from_tag('v1.4')

    assert '09f6182cef737db02a085e1d018963c7a29bde5a' == commit.hash
    with pytest.raises(IndexError):
        gr.get_commit_from_tag('v1.5')


def test_list_files_in_commit():
    gr = GitRepository('test-repos/git-1/')
    gr.checkout('a7053a4dcd627f5f4f213dc9aa002eb1caf926f8')
    files1 = gr.files()
    assert 3 == len(files1)
    gr.reset()

    gr.checkout('f0dd1308bd904a9b108a6a40865166ee962af3d4')
    files2 = gr.files()
    assert 2 == len(files2)
    gr.reset()

    gr.checkout('9e71dd5726d775fb4a5f08506a539216e878adbb')
    files3 = gr.files()
    assert 3 == len(files3)
    gr.reset()


def test_checkout_consecutive_commits():
    gr = GitRepository('test-repos/git-1/')
    gr.checkout('a7053a4dcd627f5f4f213dc9aa002eb1caf926f8')
    gr.checkout('f0dd1308bd904a9b108a6a40865166ee962af3d4')
    gr.checkout('9e71dd5726d775fb4a5f08506a539216e878adbb')
    files3 = gr.files()
    assert 3 == len(files3)
    gr.reset()


def test_checkout_with_commit_not_fully_merged_to_master():
    gr = GitRepository('test-repos/git-9/')
    gr.checkout('developing')
    files1 = gr.files()
    assert 2 == len(files1)
    gr.reset()
    assert len(gr.repo.branches) == 4, "temp branch should be cleared."
    files2 = gr.files()
    assert 1 == len(files2)
    gr.checkout('developing')
    files1 = gr.files()
    assert 2 == len(files1)
    gr.reset()


def test_get_all_commits():
    gr = GitRepository('test-repos/git-1/')
    change_sets = list(gr.get_list_commits())

    assert 13 == len(change_sets)
    assert '866e997a9e44cb4ddd9e00efe49361420aff2559' == change_sets[0].hash
    assert 'e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2' == change_sets[12].hash


def test_branches_from_commit():
    gr = GitRepository('test-repos/git-1/')
    commit = gr.get_commit('a997e9d400f742003dea601bb05a9315d14d1124')

    assert 1 == len(commit.branches)
    assert 'b2' in commit.branches

    commit = gr.get_commit('866e997a9e44cb4ddd9e00efe49361420aff2559')
    assert 2 == len(commit.branches)
    assert 'master' in commit.branches
    assert 'b2' in commit.branches


def test_other_branches_with_merge():
    gr = GitRepository('test-repos/test3/')

    commit = gr.get_commit('8cdf925bde3be3a21490d75686116b88b8263e82')
    assert commit.in_main_branch is False

    commit = gr.get_commit('189988aa490b0e5f14ed0ecb155e0e2901425d05')
    assert commit.in_main_branch is True

    commit = gr.get_commit('17bfb3f02331a7ce770e0a6b90584cdd473c6993')
    assert commit.in_main_branch is True

    commit = gr.get_commit('b5c103c7f61d05b9a35364f1923ceacc9afe7ed9')
    assert commit.in_main_branch is True
    assert commit.merge is True


def test_commit_in_master_branch():
    gr = GitRepository('test-repos/git-2/')
    assert '29e929fbc5dc6a2e9c620069b24e2a143af4285f' == gr.get_head().hash

    gr.checkout('8986af2a679759e5a15794f6d56e6d46c3f302f1')

    git_to_change_head = GitRepository('test-repos/git-2/')
    commit = git_to_change_head.get_commit('8169f76a3d7add54b4fc7bca7160d1f1eede6eda')
    assert False == commit.in_main_branch

    commit = git_to_change_head.get_commit('168b3aab057ed61a769acf336a4ef5e64f76c9fd')
    assert True == commit.in_main_branch

    gr.reset()
    assert '29e929fbc5dc6a2e9c620069b24e2a143af4285f' == gr.get_head().hash


def test_should_detail_a_commit():
    gr = GitRepository('test-repos/git-1/')
    commit = gr.get_commit('866e997a9e44cb4ddd9e00efe49361420aff2559')

    assert "Maurício Aniche" == commit.author.name
    assert "mauricioaniche@gmail.com" == commit.author.email

    assert "Matricula adicionada" == commit.msg
    assert 1 == len(commit.modifications)

    assert "Matricula.java" == commit.modifications[0].new_path
    assert True == commit.modifications[0].diff.startswith("@@ -0,0 +1,62 @@\n+package model;")
    assert True == commit.modifications[0].source_code.startswith("package model;")


def test_merge_commits():
    gr = GitRepository('test-repos/git-2/')
    commit = gr.get_commit("168b3aab057ed61a769acf336a4ef5e64f76c9fd")
    assert False == commit.merge

    commit = gr.get_commit("8169f76a3d7add54b4fc7bca7160d1f1eede6eda")
    assert False == commit.merge

    commit = gr.get_commit("29e929fbc5dc6a2e9c620069b24e2a143af4285f")
    assert True == commit.merge


def test_number_of_modifications():
    gr = GitRepository('test-repos/git-1/')
    commit = gr.get_commit('866e997a9e44cb4ddd9e00efe49361420aff2559')
    assert 62 == commit.modifications[0].added
    assert 0 == commit.modifications[0].removed

    commit = gr.get_commit('d11dd6734ff4e60cac3a7b58d9267f138c9e05c7')
    assert 1 == commit.modifications[0].added
    assert 1 == commit.modifications[0].removed


def test_modification_status():
    gr = GitRepository('test-repos/git-1/')
    commit = gr.get_commit('866e997a9e44cb4ddd9e00efe49361420aff2559')
    assert ModificationType.ADD == commit.modifications[0].change_type
    assert None == commit.modifications[0].old_path

    commit = gr.get_commit('57dbd017d1a744b949e7ca0b1c1a3b3dd4c1cbc1')
    assert ModificationType.MODIFY == commit.modifications[0].change_type
    assert commit.modifications[0].old_path == commit.modifications[0].new_path

    commit = gr.get_commit('ffccf1e7497eb8136fd66ed5e42bef29677c4b71')
    assert ModificationType.DELETE == commit.modifications[0].change_type
    assert None == commit.modifications[0].new_path


def test_diffs():
    gr = GitRepository('test-repos/test4/')
    commit = gr.get_commit('93b4b18673ca6fb5d563bbf930c45cd1198e979b')

    assert 2 == len(commit.modifications)

    for mod in commit.modifications:
        if mod.filename == 'file4.java':
            assert 8 == mod.removed
            assert 0 == mod.added

        if mod.filename == 'file2.java':
            assert 12 == mod.removed
            assert 0 == mod.added


def test_detail_rename():
    gr = GitRepository('test-repos/git-1/')
    commit = gr.get_commit('f0dd1308bd904a9b108a6a40865166ee962af3d4')

    assert "Maurício Aniche" == commit.author.name
    assert "mauricioaniche@gmail.com", commit.author.email

    assert "Matricula.javax" == commit.modifications[0].new_path
    assert "Matricula.java" == commit.modifications[0].old_path


def test_parent_commits():
    gr = GitRepository('test-repos/git-5/')
    merge_commit = gr.get_commit('5d9d79607d7e82b6f236aa29be4ba89a28fb4f15')
    assert 2 == len(merge_commit.parents)
    assert 'fa8217c324e7fb46c80e1ddf907f4e141449637e' in merge_commit.parents
    assert 'ff663cf1931a67d5e47b75fc77dcea432c728052' in merge_commit.parents

    normal_commit = gr.get_commit('ff663cf1931a67d5e47b75fc77dcea432c728052')
    assert 1 == len(normal_commit.parents)
    assert '4a17f31c0d1285477a3a467d0bc3cb38e775097d' in normal_commit.parents


def test_tags():
    gr = GitRepository('test-repos/git-8/')
    commit = gr.get_commit_from_tag('tag1')
    assert '6bb9e2c6a8080e6b5b34e6e316c894b2ddbf7fcd' == commit.hash

    commit = gr.get_commit_from_tag('tag2')
    assert '4638730126d40716e230c2040751a13153fb1556' == commit.hash

    with pytest.raises(IndexError):
        gr.get_commit_from_tag('tag4')


def test_get_commits_last_modified_lines_simple():
    gr = GitRepository('test-repos/test5/')

    buggy_commits = gr.get_commits_last_modified_lines(gr.get_commit('e6d3b38a9ef683e8184eac10a0471075c2808bbd'))

    assert len(buggy_commits) == 1
    assert '540c7f31c18664a38190fafb6721b5174ff4a166' in buggy_commits


def test_get_commits_last_modified_lines_multiple():
    gr = GitRepository('test-repos/test5/')

    buggy_commits = gr.get_commits_last_modified_lines(gr.get_commit('9942ee9dcdd1103e5808d544a84e6bc8cade0e54'))

    assert len(buggy_commits) == 3
    assert '2eb905e5e7be414fd184d6b4f1571b142621f4de' in buggy_commits
    assert '20a40688521c1802569e60f9d55342c3bfdd772c' in buggy_commits
    assert '22505e97dca6f843549b3a484b3609be4e3acf17' in buggy_commits


def test_get_commits_last_modified_lines_rename_simple():
    gr = GitRepository('test-repos/test5/')

    buggy_commits = gr.get_commits_last_modified_lines(gr.get_commit('45ba0a61ccc448625bce0fea0301cf0c1ab32696'))

    assert len(buggy_commits) == 1
    assert 'e358878a00e78aca8366264d61a7319d00dd8186' in buggy_commits


def test_get_commits_last_modified_lines_multiple_rename():
    gr = GitRepository('test-repos/test5/')
    # in this case the algorithm doesn't work because the file has been renamed 2 times!

    buggy_commits = gr.get_commits_last_modified_lines(gr.get_commit('9e858753b3d69f560cf72aaaa297f2608145ebcf'))
    assert len(buggy_commits) == 0


def test_get_commits_last_modified_lines_rename_simple_more_commits():
    gr = GitRepository('test-repos/test5/')

    buggy_commits = gr.get_commits_last_modified_lines(gr.get_commit('4e287ab8e6dba110219404fb8a43993f3dda674c'))
    assert len(buggy_commits) == 1
    assert '06b9ff31cd3475d9fd9ef668cc0844ab169da726' in buggy_commits


def test_get_commits_last_modified_lines_useless_lines():
    gr = GitRepository('test-repos/test5/')

    buggy_commits = gr.get_commits_last_modified_lines(gr.get_commit('3bc7295c16b7dfc15d5f82eb6962a2774e1b8420'))
    assert len(buggy_commits) == 1
    assert 'c7fc2e870ce03b0b8dc29ed0eeb26d14e235ea3b' in buggy_commits


def test_get_commits_last_modified_lines_useless_lines2():
    gr = GitRepository('test-repos/test5/')

    buggy_commits = gr.get_commits_last_modified_lines(gr.get_commit('4155c421ee5cbb3c34feee7b68aa78a2ee1bbeae'))
    assert len(buggy_commits) == 0


def test_get_commits_last_modified_lines_for_single_file():
    gr = GitRepository('test-repos/test5/')

    commit = gr.get_commit('0f726924f96621e4965039123098ba83e39ffba6')
    buggy_commits = None
    for mod in commit.modifications:
        if mod.filename == 'A.java':
            buggy_commits = gr.get_commits_last_modified_lines(commit, mod)

    assert len(buggy_commits) == 1
    assert 'e2ed043eb96c05ebde653a44ae733ded9ef90750' in buggy_commits


def test_get_commits_last_modified_lines_with_more_modification():
    gr = GitRepository('test-repos/test5/')

    buggy_commits = gr.get_commits_last_modified_lines(gr.get_commit('c7002fb321a8ba32a28fac200538f7c2ba76f175'))
    assert len(buggy_commits) == 1
    assert '5cb9e9ae44a0949ec91d06a955975289be766f34' in buggy_commits
