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

import pytest

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

from pydriller.repository_mining import RepositoryMining


def test_mod_with_file_types():
    lc = list(RepositoryMining('test-repos/git-4/', only_modifications_with_file_types=['.java']).traverse_commits())

    assert 2 == len(lc)
    assert 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5' == lc[0].hash
    assert 'b8c2be250786975f1c6f47e96922096f1bb25e39' == lc[1].hash


def test_only_in_main_branch():
    lc = list(RepositoryMining('test-repos/git-5/').traverse_commits())

    assert 5 == len(lc)
    assert '4a17f31c0d1285477a3a467d0bc3cb38e775097d' == lc[0].hash
    assert 'ff663cf1931a67d5e47b75fc77dcea432c728052' == lc[1].hash
    assert 'fa8217c324e7fb46c80e1ddf907f4e141449637e' == lc[2].hash
    assert '5d9d79607d7e82b6f236aa29be4ba89a28fb4f15' == lc[3].hash
    assert '377e0f474d70f6205784d0150ee0069a050c29ed' == lc[4].hash


def test_multiple_filters():
    lc = list(RepositoryMining('test-repos/git-5/', only_no_merge=True).traverse_commits())

    assert 4 == len(lc)
    assert '4a17f31c0d1285477a3a467d0bc3cb38e775097d' == lc[0].hash
    assert 'ff663cf1931a67d5e47b75fc77dcea432c728052' == lc[1].hash
    assert 'fa8217c324e7fb46c80e1ddf907f4e141449637e' == lc[2].hash
    assert '377e0f474d70f6205784d0150ee0069a050c29ed' == lc[3].hash


def test_no_filters():
    lc = list(RepositoryMining('test-repos/git-4/').traverse_commits())

    assert 3 == len(lc)
    assert 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5' == lc[0].hash
    assert '375de7a8275ecdc0b28dc8de2568f47241f443e9' == lc[1].hash
    assert 'b8c2be250786975f1c6f47e96922096f1bb25e39' == lc[2].hash


def test_no_single_commit():
    with pytest.raises(Exception):
        for commit in RepositoryMining('test-repos/git-5',
                                       single="6fe83d9fbf9a63cc1c51e5fe6fd5230f7fbbce6f").traverse_commits():
            print(commit.hash)


def test_only_in_branch():
    lc = list(RepositoryMining('test-repos/git-5/', only_in_branch='branch2').traverse_commits())
    assert 6 == len(lc)

    assert '4a17f31c0d1285477a3a467d0bc3cb38e775097d' == lc[0].hash
    assert 'ff663cf1931a67d5e47b75fc77dcea432c728052' == lc[1].hash
    assert 'fa8217c324e7fb46c80e1ddf907f4e141449637e' == lc[2].hash
    assert '5d9d79607d7e82b6f236aa29be4ba89a28fb4f15' == lc[3].hash
    assert '377e0f474d70f6205784d0150ee0069a050c29ed' == lc[4].hash
    assert '6fe83d9fbf9a63cc1c51e5fe6fd5230f7fbbce6f' == lc[5].hash


def test_only_in_branches():
    # by default, only analyze master
    assert 3 == len(list(RepositoryMining('test-repos/test8/').traverse_commits()))
    # only analyze b2
    assert 4 == len(list(RepositoryMining('test-repos/test8/', only_in_branch='b2').traverse_commits()))
    # only analyze b1
    assert 5 == len(list(RepositoryMining('test-repos/test8/', only_in_branch='b1').traverse_commits()))


def test_only_in_branch_not_exist():
    with pytest.raises(Exception):
        list(RepositoryMining('test-repos/git-5/', only_in_branch='branch7').traverse_commits())


def test_only_authors():
    lc = list(RepositoryMining('test-repos/git-10/', only_authors=["Maurício Aniche"]).traverse_commits())
    assert 4 == len(lc)

    lc = list(RepositoryMining('test-repos/git-10/', only_authors=["ishepard"]).traverse_commits())
    assert 1 == len(lc)


def test_only_commits():
    # 4e669cb4f69245dc669e116517d80d038d8e0434
    # 29e929fbc5dc6a2e9c620069b24e2a143af4285f
    # 8986af2a679759e5a15794f6d56e6d46c3f302f1
    # 8169f76a3d7add54b4fc7bca7160d1f1eede6eda
    # 168b3aab057ed61a769acf336a4ef5e64f76c9fd
    lc = list(RepositoryMining('test-repos/git-10/',
                               only_commits=["4e669cb4f69245dc669e116517d80d038d8e0434"]).traverse_commits())
    assert 1 == len(lc)
    assert "4e669cb4f69245dc669e116517d80d038d8e0434" == lc[0].hash

    lc = list(RepositoryMining('test-repos/git-10/',
                               only_commits=["4e669cb4f69245dc669e116517d80d038d8e0434",
                                             "8986af2a679759e5a15794f6d56e6d46c3f302f1"]).traverse_commits())
    assert 2 == len(lc)
    assert "8986af2a679759e5a15794f6d56e6d46c3f302f1" == lc[0].hash
    assert "4e669cb4f69245dc669e116517d80d038d8e0434" == lc[1].hash

    lc = list(RepositoryMining('test-repos/git-10/',
                               only_commits=["4e669cb4f69245dc669e116517d80d038d8e0434",
                                             "8986af2a679759e5a15794f6d56e6d46c3f302f1",
                                             "29e929fbc5dc6a2e9c620069b24e2a143af4285f"]).traverse_commits())
    assert 3 == len(lc)
    assert "8986af2a679759e5a15794f6d56e6d46c3f302f1" == lc[0].hash
    assert "29e929fbc5dc6a2e9c620069b24e2a143af4285f" == lc[1].hash
    assert "4e669cb4f69245dc669e116517d80d038d8e0434" == lc[2].hash

    lc = list(RepositoryMining('test-repos/git-10/', only_commits=["fake hash"]).traverse_commits())
    assert 0 == len(lc)

    only_commits = len(list(RepositoryMining('test-repos/git-10/',
                                     only_commits=["4e669cb4f69245dc669e116517d80d038d8e0434",
                                                   "29e929fbc5dc6a2e9c620069b24e2a143af4285f",
                                                   "8986af2a679759e5a15794f6d56e6d46c3f302f1",
                                                   "8169f76a3d7add54b4fc7bca7160d1f1eede6eda",
                                                   "168b3aab057ed61a769acf336a4ef5e64f76c9fd"]).traverse_commits()))

    total_commits = len(list(RepositoryMining('test-repos/git-10/').traverse_commits()))

    assert only_commits == total_commits
