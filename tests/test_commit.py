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

from pydriller.domain.commit import Modification, ModificationType

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

import pytest
from pathlib import Path
from pydriller.git_repository import GitRepository
from datetime import timezone

@pytest.yield_fixture(scope="module")
def resource():
    yield GitRepository('test-repos/git-1/')


def test_equal(resource):
    c1 = resource.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2')
    c2 = resource.get_commit(c1.parents[0])
    c3 = resource.get_commit('a4ece0762e797d2e2dcbd471115108dd6e05ff58')

    assert c1.parents[0] == 'a4ece0762e797d2e2dcbd471115108dd6e05ff58'
    assert c3 == c2
    assert c1 != c3


def test_filename():
    diff_and_sc = {
        'diff': '',
        'source_code': '',
        'source_code_before': ''
    }
    m1 = Modification('dspadini/pydriller/myfile.py',
                      'dspadini/pydriller/mynewfile.py',
                      ModificationType.ADD, diff_and_sc)
    m3 = Modification('dspadini/pydriller/myfile.py',
                      'dspadini/pydriller/mynewfile.py',
                      ModificationType.ADD, diff_and_sc)
    m2 = Modification('dspadini/pydriller/myfile.py',
                      None,
                      ModificationType.ADD, diff_and_sc)

    assert m1.filename == 'mynewfile.py'
    assert m2.filename == 'myfile.py'
    assert m1 != m2
    assert m3 == m1


def test_metrics_python():
    with open('test-repos/test6/git_repository.py') as f:
        sc = f.read()

    diff_and_sc = {
        'diff': '',
        'source_code': sc,
        'source_code_before': sc
    }

    m1 = Modification('test-repos/test6/git_repository.py',
                      "test-repos/test6/git_repository.py",
                      ModificationType.MODIFY, diff_and_sc)

    assert m1.nloc == 196
    assert m1.token_count == 1009
    assert m1.complexity == 43

    assert len(m1.methods) == 19


def test_metrics_cpp():
    with open('test-repos/test6/FileCPP.cpp') as f:
        sc = f.read()

    diff_and_sc = {
        'diff': '',
        'source_code': sc,
        'source_code_before': sc
    }

    m1 = Modification('test-repos/test6/FileCPP.cpp',
                      "test-repos/test6/FileCPP.cpp",
                      ModificationType.MODIFY, diff_and_sc)

    assert m1.nloc == 793
    assert m1.token_count == 5564
    assert m1.complexity == 199

    assert len(m1.methods) == 16


def test_metrics_java():
    with open('test-repos/test6/FileJava.java') as f:
        sc = f.read()

    diff_and_sc = {
        'diff': '',
        'source_code': sc,
        'source_code_before': sc
    }

    m1 = Modification('test-repos/test6/FileJava.java',
                      "test-repos/test6/FileJava.java",
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

    m1 = Modification('test-repos/test6/NotSupported.pdf',
                      "test-repos/test6/NotSupported.pdf",
                      ModificationType.MODIFY, diff_and_sc)

    assert m1.nloc == 2
    assert len(m1.methods) == 0


def test_filepahs():
    gr = GitRepository('test-repos/test7')
    c = gr.get_commit('f0f8aea2db50ed9f16332d86af3629ff7780583e')

    mod0 = c.modifications[0]

    assert mod0.filename == 'a.java'
    assert mod0.new_path == str(Path('dir2/a.java'))
    assert mod0.old_path == str(Path('dir2/a.java'))


def test_projectname():
    gr = GitRepository('test-repos/test7')
    c = gr.get_commit('f0f8aea2db50ed9f16332d86af3629ff7780583e')

    assert c.project_name == 'test7'


def test_modification_type_unknown():
    gr = GitRepository('test-repos/git-11')
    c = gr.get_commit('1734d6da01378bad3aade12b52bb4aa8954835dc')

    mod0 = c.modifications[0]

    assert mod0.change_type.name == 'UNKNOWN'

    
def test_modification_with_more_parents():
    gr = GitRepository('test-repos/test11')
    c = gr.get_commit('ce6bcd987a6a53cc55da7cef9f8bb128adf68741')
    assert len(c.modifications) == 0

    c = gr.get_commit('1b03d13c816f576eb82a8c3e935fbcacff6c2e8d')
    assert len(c.modifications) == 0


def test_eq_commit():
    gr = GitRepository('test-repos/git-11')
    c1 = gr.get_commit('1734d6da01378bad3aade12b52bb4aa8954835dc')
    c2 = gr.get_commit('2c1327f957ba3b2a5e86eaed097b0a425236719e')
    c3 = gr.get_commit('1734d6da01378bad3aade12b52bb4aa8954835dc')
    m1 = gr.get_commit('1734d6da01378bad3aade12b52bb4aa8954835dc'
                       '').modifications[0]
    assert c1 == c3
    assert c1 == c1
    assert c1 != m1
    assert c1 != c2


def test_eq_modifications():
    gr = GitRepository('test-repos/git-1')
    m1 = gr.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2'
                       '').modifications[0]
    m2 = gr.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2'
                       '').modifications[0]
    m3 = gr.get_commit('a4ece0762e797d2e2dcbd471115108dd6e05ff58'
                       '').modifications[0]
    c1 = gr.get_commit('a4ece0762e797d2e2dcbd471115108dd6e05ff58')

    assert m1 == m2
    assert m1 == m1
    assert m1 != m3
    assert m1 != c1


def test_tzoffset():
    gr = GitRepository('test-repos/git-1')
    tz1 = gr.get_commit(
        'e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2').author_timezone
    tz2 = gr.get_commit(
        'e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2').committer_timezone
    assert tz1 == 10800 # -3 hours
    assert tz2 == 10800 # -3 hours

    gr = GitRepository('test-repos/test1')
    tz1 = gr.get_commit(
        'da39b1326dbc2edfe518b90672734a08f3c13458').author_timezone
    tz2 = gr.get_commit(
        'da39b1326dbc2edfe518b90672734a08f3c13458').committer_timezone
    assert tz1 == -7200 # +2 hours
    assert tz2 == -7200 # +2 hours


def test_source_code_before():
    gr = GitRepository('test-repos/git-1')
    m1 = gr.get_commit('ffccf1e7497eb8136fd66ed5e42bef29677c4b71'
                       '').modifications[0]

    assert m1.source_code is None
    assert m1.source_code_before is not None


def test_source_code_before_complete():
    gr = GitRepository('test-repos/test12')
    m1 = gr.get_commit('ca1f75455f064410360bc56218d0418221cf9484'
                       '').modifications[0]

    with open('test-repos/test12/sc_A_ca1f75455f064410360bc56218d0418221cf9484'
              '.txt') as f:
        sc = f.read()

    assert m1.source_code == sc
    assert m1.source_code_before is None

    old_sc = sc
    with open(
            'test-repos/test12/sc_A_022ebf5fba835c6d95e99eaccc2d85b3db5a2ec0'
            '.txt') as f:
        sc = f.read()

    m1 = gr.get_commit('022ebf5fba835c6d95e99eaccc2d85b3db5a2ec0'
                       '').modifications[0]

    assert m1.source_code == sc
    assert m1.source_code_before == old_sc

    old_sc = sc
    m1 = gr.get_commit('ecd6780457835a2fc85c532338a29f2c98a6cfeb'
                       '').modifications[0]

    assert m1.source_code is None
    assert m1.source_code_before == old_sc
