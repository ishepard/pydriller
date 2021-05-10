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
from pydriller.git import Git
from pathlib import Path
import pytest
import logging

from pydriller.domain.commit import ModifiedFile, ModificationType

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


@pytest.fixture
def repo(request):
    gr = Git(request.param)
    yield gr
    gr.clear()


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_equal(repo: Git):
    c1 = repo.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2')
    c2 = repo.get_commit(c1.parents[0])
    c3 = repo.get_commit('a4ece0762e797d2e2dcbd471115108dd6e05ff58')

    assert c1.parents[0] == 'a4ece0762e797d2e2dcbd471115108dd6e05ff58'
    assert c3 == c2
    assert c1 != c3


def test_filename():
    diff_and_sc = {
        'diff': '',
        'source_code': '',
        'source_code_before': ''
    }
    m1 = ModifiedFile('dspadini/pydriller/myfile.py',
                      'dspadini/pydriller/mynewfile.py',
                      ModificationType.ADD, diff_and_sc)
    m3 = ModifiedFile('dspadini/pydriller/myfile.py',
                      'dspadini/pydriller/mynewfile.py',
                      ModificationType.ADD, diff_and_sc)
    m2 = ModifiedFile('dspadini/pydriller/myfile.py',
                      None,
                      ModificationType.ADD, diff_and_sc)

    assert m1.filename == 'mynewfile.py'
    assert m2.filename == 'myfile.py'
    assert m1 != m2
    assert m3 == m1


def test_metrics_python():
    with open('test-repos/lizard/git_repository.py') as f:
        sc = f.read()

    diff_and_sc = {
        'diff': '',
        'source_code': sc,
        'source_code_before': sc
    }

    m1 = ModifiedFile('test-repos/lizard/git_repository.py',
                      "test-repos/lizard/git_repository.py",
                      ModificationType.MODIFY, diff_and_sc)

    assert m1.nloc == 196
    assert m1.token_count == 1009
    assert m1.complexity == 43

    assert len(m1.methods) == 19


def test_changed_methods():

    gr = Git("test-repos/diff")

    # add a new method
    mod = gr.get_commit(
        'ea95227e0fd128aa69c7ab6a8ac485f72251b3ed').modified_files[0]
    assert len(mod.changed_methods) == 1
    assert mod.changed_methods[0].name == 'GitRepository::singleProjectThirdMethod'

    # add 2 new methods
    mod = gr.get_commit(
        'd8eb8e80b671246a43c98d97b05f6d1c5ada14fb').modified_files[0]
    assert len(mod.changed_methods) == 2

    # remove one method
    mod = gr.get_commit(
        '0c8f9fdec926785198b399a2c49adb5884aa952c').modified_files[0]
    assert len(mod.changed_methods) == 1

    # add and remove one one method at different locations
    mod = gr.get_commit(
        'd8bb142c5616041b71cbfaa11eeb768d9a1a296e').modified_files[0]
    assert len(mod.changed_methods) == 2

    # add and remove one one method at the same location
    # this is equivalent to replacing a method - although we expect 2 methods
    mod = gr.get_commit(
        '9e9473d5ca310b7663e9df93c402302b6b7f24aa').modified_files[0]
    assert len(mod.changed_methods) == 2

    # update a method
    mod = gr.get_commit(
        'b267a14e0503fdac36d280422f16360d1f661f12').modified_files[0]
    assert len(mod.changed_methods) == 1

    # update and add a new method
    mod = gr.get_commit(
        '2489099dfd90edb99ddc2c82b62524b66c07c687').modified_files[0]
    assert len(mod.changed_methods) == 2

    # update and delete methods
    mod = gr.get_commit(
        '5aebeb30e0238543a93e5bed806639481460cd9a').modified_files[0]
    assert len(mod.changed_methods) == 2

    # delete 3 methods (test cleanup - revert the test file to its
    # initial set of methods)
    mod = gr.get_commit(
        '9f6ddc2aac740a257af59a76860590cb8a84c77b').modified_files[0]
    assert len(mod.changed_methods) == 3


def test_metrics_cpp():
    with open('test-repos/lizard/FileCPP.cpp') as f:
        sc = f.read()

    diff_and_sc = {
        'diff': '',
        'source_code': sc,
        'source_code_before': sc
    }

    m1 = ModifiedFile('test-repos/lizard/FileCPP.cpp',
                      "test-repos/lizard/FileCPP.cpp",
                      ModificationType.MODIFY, diff_and_sc)

    assert m1.nloc == 793
    assert m1.token_count == 5564
    assert m1.complexity == 199

    assert len(m1.methods) == 16


def test_metrics_java():
    with open('test-repos/lizard/FileJava.java') as f:
        sc = f.read()

    diff_and_sc = {
        'diff': '',
        'source_code': sc,
        'source_code_before': sc
    }

    m1 = ModifiedFile('test-repos/lizard/FileJava.java',
                      "test-repos/lizard/FileJava.java",
                      ModificationType.MODIFY, diff_and_sc)

    assert m1.nloc == 466
    assert m1.token_count == 3809
    assert m1.complexity == 92

    assert len(m1.methods) == 46


def test_metrics_not_supported_file():
    sc = 'asd !&%@*&^@\n jjdkj'

    diff_and_sc = {
        'diff': '',
        'source_code': sc,
        'source_code_before': sc
    }

    m1 = ModifiedFile('test-repos/lizard/NotSupported.pdf',
                      "test-repos/lizard/NotSupported.pdf",
                      ModificationType.MODIFY, diff_and_sc)

    assert m1.nloc is None


@pytest.mark.parametrize('repo', ['test-repos/files_in_directories'], indirect=True)
def test_filepahs(repo: Git):
    c = repo.get_commit('f0f8aea2db50ed9f16332d86af3629ff7780583e')

    mod0 = c.modified_files[0]

    assert mod0.filename == 'a.java'
    assert mod0.new_path == str(Path('dir2/a.java'))
    assert mod0.old_path == str(Path('dir2/a.java'))


@pytest.mark.parametrize('repo', ['test-repos/files_in_directories'], indirect=True)
def test_projectname(repo: Git):
    c = repo.get_commit('f0f8aea2db50ed9f16332d86af3629ff7780583e')

    assert c.project_name == 'files_in_directories'


@pytest.mark.parametrize('repo', ['test-repos/files_in_directories'], indirect=True)
def test_projectpath(repo: Git):
    c = repo.get_commit('f0f8aea2db50ed9f16332d86af3629ff7780583e')

    assert c.project_path.endswith('files_in_directories') is True


@pytest.mark.parametrize('repo', ['test-repos/unknown_modification'], indirect=True)
def test_modification_type_unknown(repo: Git):
    c = repo.get_commit('1734d6da01378bad3aade12b52bb4aa8954835dc')

    mod0 = c.modified_files[0]

    assert mod0.change_type.name == 'UNKNOWN'


@pytest.mark.parametrize('repo', ['test-repos/empty_modifications'], indirect=True)
def test_modification_with_more_parents(repo: Git):
    c = repo.get_commit('ce6bcd987a6a53cc55da7cef9f8bb128adf68741')
    assert len(c.modified_files) == 0

    c = repo.get_commit('1b03d13c816f576eb82a8c3e935fbcacff6c2e8d')
    assert len(c.modified_files) == 0


@pytest.mark.parametrize('repo', ['test-repos/small_repo'], indirect=True)
def test_eq_commit(repo: Git):
    c1 = repo.get_commit('6411e3096dd2070438a17b225f44475136e54e3a')
    c2 = repo.get_commit('09f6182cef737db02a085e1d018963c7a29bde5a')
    c3 = repo.get_commit('6411e3096dd2070438a17b225f44475136e54e3a')
    c4 = repo.get_commit('09f6182cef737db02a085e1d018963c7a29bde5a')
    assert c1 == c3
    assert c1 == c1
    assert c2 == c4
    assert c2 == c2
    assert c1 != c2
    assert c3 != c4


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_eq_modifications(repo: Git):
    m1 = repo.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2').modified_files[0]
    m2 = repo.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2').modified_files[0]
    m3 = repo.get_commit('a4ece0762e797d2e2dcbd471115108dd6e05ff58').modified_files[0]
    c1 = repo.get_commit('a4ece0762e797d2e2dcbd471115108dd6e05ff58')

    assert m1 == m2
    assert m1 == m1
    assert m1 != m3
    assert m1 != c1


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_tzoffset_minus_hours(repo: Git):
    tz1 = repo.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2').author_timezone
    tz2 = repo.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2').committer_timezone
    assert tz1 == 10800  # -3 hours
    assert tz2 == 10800  # -3 hours


@pytest.mark.parametrize('repo', ['test-repos/small_repo'], indirect=True)
def test_tzoffset_plus_hours(repo: Git):
    tz1 = repo.get_commit('da39b1326dbc2edfe518b90672734a08f3c13458').author_timezone
    tz2 = repo.get_commit('da39b1326dbc2edfe518b90672734a08f3c13458').committer_timezone
    assert tz1 == -7200  # +2 hours
    assert tz2 == -7200  # +2 hours


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_source_code_before(repo: Git):
    m1 = repo.get_commit('ffccf1e7497eb8136fd66ed5e42bef29677c4b71').modified_files[0]

    assert m1.source_code is None
    assert m1.source_code_before is not None


@pytest.mark.parametrize('repo', ['test-repos/source_code_before_commit'], indirect=True)
def test_source_code_before_complete(repo: Git):
    m1 = repo.get_commit('ca1f75455f064410360bc56218d0418221cf9484').modified_files[0]

    with open('test-repos/source_code_before_commit/'
              'sc_A_ca1f75455f064410360bc56218d0418221cf9484.txt') as f:
        sc = f.read()

    assert m1.source_code == sc
    assert m1.source_code_before is None

    old_sc = sc
    with open(
            'test-repos/source_code_before_commit/'
            'sc_A_022ebf5fba835c6d95e99eaccc2d85b3db5a2ec0.txt') as f:
        sc = f.read()

    m1 = repo.get_commit('022ebf5fba835c6d95e99eaccc2d85b3db5a2ec0').modified_files[0]

    assert m1.source_code == sc
    assert m1.source_code_before == old_sc

    old_sc = sc
    m1 = repo.get_commit('ecd6780457835a2fc85c532338a29f2c98a6cfeb').modified_files[0]

    assert m1.source_code is None
    assert m1.source_code_before == old_sc


@pytest.mark.parametrize('repo', ['test-repos/small_repo'], indirect=True)
def test_shortstats_all_additions(repo: Git):
    c1 = repo.get_commit('a88c84ddf42066611e76e6cb690144e5357d132c')

    assert c1.insertions == 191
    assert c1.lines == 191
    assert c1.files == 2
    assert c1.deletions == 0


@pytest.mark.parametrize('repo', ['test-repos/small_repo'], indirect=True)
def test_shortstats_all_deletions(repo: Git):
    c1 = repo.get_commit('6411e3096dd2070438a17b225f44475136e54e3a')

    assert c1.insertions == 0
    assert c1.lines == 4
    assert c1.files == 1
    assert c1.deletions == 4


@pytest.mark.parametrize('repo', ['test-repos/small_repo'], indirect=True)
def test_shortstats_rename(repo: Git):
    c1 = repo.get_commit('da39b1326dbc2edfe518b90672734a08f3c13458')

    assert c1.insertions == 0
    assert c1.lines == 3
    assert c1.files == 1
    assert c1.deletions == 3


@pytest.mark.parametrize('repo', ['test-repos/complex_repo'], indirect=True)
def test_shortstats_add_and_del(repo: Git):
    c1 = repo.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2')

    assert c1.insertions == 1
    assert c1.lines == 2
    assert c1.files == 1
    assert c1.deletions == 1
