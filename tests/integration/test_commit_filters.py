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
from datetime import datetime, timezone, timedelta

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

from pydriller.repository_mining import RepositoryMining


def test_mod_with_file_types():
    lc = list(RepositoryMining('test-repos/git-4/',
                               only_modifications_with_file_types=['.java'])
              .traverse_commits())

    assert len(lc) == 2
    assert lc[0].hash == 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5'
    assert lc[1].hash == 'b8c2be250786975f1c6f47e96922096f1bb25e39'

    lc = list(RepositoryMining('test-repos/git-7/',
                               only_modifications_with_file_types=['.java'])
              .traverse_commits())

    assert len(lc) == 2
    assert lc[0].hash == '5adbb71167e79ab6b974827e74c9da4d81977655'
    assert lc[1].hash == '0577bec2387ee131e1ccf336adcc172224d3f6f9'


def test_mod_with_file_types_no_extension():
    lc = list(RepositoryMining('test-repos/git-4/',
                               only_modifications_with_file_types=['.py'])
              .traverse_commits())

    assert len(lc) == 0


def test_mod_with_file_types_and_date():
    to_zone = timezone(timedelta(hours=2))
    dt1 = datetime(2016, 10, 8, 23, 57, 49, tzinfo=to_zone)
    print(dt1)
    lc = list(RepositoryMining('test-repos/git-4/',
                               only_modifications_with_file_types=['.java'],
                               since=dt1)
              .traverse_commits())

    print(lc)
    assert len(lc) == 1
    assert lc[0].hash == 'b8c2be250786975f1c6f47e96922096f1bb25e39'


def test_only_in_main_branch():
    lc = list(RepositoryMining('test-repos/git-5/').traverse_commits())

    assert len(lc) == 5
    assert lc[0].hash == '4a17f31c0d1285477a3a467d0bc3cb38e775097d'
    assert lc[1].hash == 'ff663cf1931a67d5e47b75fc77dcea432c728052'
    assert lc[2].hash == 'fa8217c324e7fb46c80e1ddf907f4e141449637e'
    assert lc[3].hash == '5d9d79607d7e82b6f236aa29be4ba89a28fb4f15'
    assert lc[4].hash == '377e0f474d70f6205784d0150ee0069a050c29ed'


def test_only_no_merge():
    lc = list(RepositoryMining('test-repos/git-5/',
                               only_no_merge=True).traverse_commits())

    assert len(lc) == 4
    assert lc[0].hash == '4a17f31c0d1285477a3a467d0bc3cb38e775097d'
    assert lc[1].hash == 'ff663cf1931a67d5e47b75fc77dcea432c728052'
    assert lc[2].hash == 'fa8217c324e7fb46c80e1ddf907f4e141449637e'
    assert lc[3].hash == '377e0f474d70f6205784d0150ee0069a050c29ed'


def test_no_filters():
    lc = list(RepositoryMining('test-repos/git-4/').traverse_commits())

    assert len(lc) == 3
    assert lc[0].hash == 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5'
    assert lc[1].hash == '375de7a8275ecdc0b28dc8de2568f47241f443e9'
    assert lc[2].hash == 'b8c2be250786975f1c6f47e96922096f1bb25e39'


def test_only_in_branch():
    lc = list(RepositoryMining('test-repos/git-5/',
                               only_in_branch='branch2').traverse_commits())
    assert len(lc) == 6

    assert lc[0].hash == '4a17f31c0d1285477a3a467d0bc3cb38e775097d'
    assert lc[1].hash == 'ff663cf1931a67d5e47b75fc77dcea432c728052'
    assert lc[2].hash == 'fa8217c324e7fb46c80e1ddf907f4e141449637e'
    assert lc[3].hash == '5d9d79607d7e82b6f236aa29be4ba89a28fb4f15'
    assert lc[4].hash == '377e0f474d70f6205784d0150ee0069a050c29ed'
    assert lc[5].hash == '6fe83d9fbf9a63cc1c51e5fe6fd5230f7fbbce6f'


def test_only_in_branches():
    # by default, only analyze master
    assert len(list(RepositoryMining('test-repos/test8/')
                    .traverse_commits())) == 3
    # only analyze b2
    assert len(list(RepositoryMining('test-repos/test8/', only_in_branch='b2')
                    .traverse_commits())) == 4
    # only analyze b1
    assert len(list(RepositoryMining('test-repos/test8/', only_in_branch='b1')
                    .traverse_commits())) == 5


def test_only_in_branch_not_exist():
    with pytest.raises(Exception):
        list(RepositoryMining('test-repos/git-5/', only_in_branch='branch7')
             .traverse_commits())


def test_only_authors():
    lc = list(RepositoryMining('test-repos/git-10/',
                               only_authors=["Maurício Aniche"])
              .traverse_commits())
    assert len(lc) == 4

    lc = list(RepositoryMining('test-repos/git-10/',
                               only_authors=["ishepard"])
              .traverse_commits())
    assert len(lc) == 1


def test_only_authors_not_existing():
    lc = list(RepositoryMining('test-repos/git-10/',
                               only_authors=["Uncle Bob"])
              .traverse_commits())
    assert len(lc) == 0


def test_only_commits():
    # 4e669cb4f69245dc669e116517d80d038d8e0434
    # 29e929fbc5dc6a2e9c620069b24e2a143af4285f
    # 8986af2a679759e5a15794f6d56e6d46c3f302f1
    # 8169f76a3d7add54b4fc7bca7160d1f1eede6eda
    # 168b3aab057ed61a769acf336a4ef5e64f76c9fd
    lc = list(RepositoryMining('test-repos/git-10/',
                               only_commits=["4e669cb4f69245dc669e116517d80d038d8e0434"]).traverse_commits())
    assert len(lc) == 1
    assert lc[0].hash == "4e669cb4f69245dc669e116517d80d038d8e0434"

    lc = list(RepositoryMining('test-repos/git-10/',
                               only_commits=["4e669cb4f69245dc669e116517d80d038d8e0434",
                                             "8986af2a679759e5a15794f6d56e6d46c3f302f1"]).traverse_commits())
    assert len(lc) == 2
    assert lc[0].hash == "8986af2a679759e5a15794f6d56e6d46c3f302f1"
    assert lc[1].hash == "4e669cb4f69245dc669e116517d80d038d8e0434"

    lc = list(RepositoryMining('test-repos/git-10/',
                               only_commits=["4e669cb4f69245dc669e116517d80d038d8e0434",
                                             "8986af2a679759e5a15794f6d56e6d46c3f302f1",
                                             "29e929fbc5dc6a2e9c620069b24e2a143af4285f"]).traverse_commits())
    assert len(lc) == 3
    assert lc[0].hash == "8986af2a679759e5a15794f6d56e6d46c3f302f1"
    assert lc[1].hash == "29e929fbc5dc6a2e9c620069b24e2a143af4285f"
    assert lc[2].hash == "4e669cb4f69245dc669e116517d80d038d8e0434"

    lc = list(RepositoryMining('test-repos/git-10/',
                               only_commits=["fake hash"]).traverse_commits())
    assert len(lc) == 0

    only_commits = len(list(RepositoryMining('test-repos/git-10/',
                                             only_commits=["4e669cb4f69245dc669e116517d80d038d8e0434",
                                                           "29e929fbc5dc6a2e9c620069b24e2a143af4285f",
                                                           "8986af2a679759e5a15794f6d56e6d46c3f302f1",
                                                           "8169f76a3d7add54b4fc7bca7160d1f1eede6eda",
                                                           "168b3aab057ed61a769acf336a4ef5e64f76c9fd"]).traverse_commits()))

    total_commits = len(list(RepositoryMining('test-repos/git-10/').traverse_commits()))

    assert total_commits == only_commits


def test_single_commit():
    lc = list(RepositoryMining('test-repos/git-10/',
                               single="4e669cb4f69245dc669e116517d80d038d8e0434").traverse_commits())
    assert len(lc) == 1
    assert lc[0].hash == "4e669cb4f69245dc669e116517d80d038d8e0434"

    lc = list(RepositoryMining('test-repos/git-10/',
                               single="168b3aab057ed61a769acf336a4ef5e64f76c9fd").traverse_commits())
    assert len(lc) == 1
    assert lc[0].hash == "168b3aab057ed61a769acf336a4ef5e64f76c9fd"


def test_filepath_with_to():
    dt = datetime(2018, 6, 6)
    assert len(list(RepositoryMining(
        path_to_repo='test-repos/test5',
        filepath='myfolder/A.java',
        to=dt).traverse_commits())) == 4


def test_filepath_with_since():
    since = datetime(2018, 6, 6)
    assert len(list(RepositoryMining(
        path_to_repo='test-repos/test5',
        filepath='myfolder/A.java',
        since=since).traverse_commits())) == 10


def test_filepath_with_rename():
    dt = datetime(2018, 6, 6)
    commits = list(RepositoryMining(
        path_to_repo='test-repos/test1',
        filepath='file4.java',
        to=dt).traverse_commits())
    assert len(commits) == 2

    commit_hashes = [commit.hash for commit in commits]

    assert 'da39b1326dbc2edfe518b90672734a08f3c13458' in commit_hashes
    assert 'a88c84ddf42066611e76e6cb690144e5357d132c' in commit_hashes


def test_filepath_with_rename_complex():
    commits = list(RepositoryMining(
        path_to_repo='test-repos/git-1',
        filepath='Matricula.javax').traverse_commits())
    assert len(commits) == 6

    commit_hashes = [commit.hash for commit in commits]

    assert 'f0dd1308bd904a9b108a6a40865166ee962af3d4' in commit_hashes
    assert '953737b199de233896f00b4d87a0bc2794317253' in commit_hashes
    assert 'a3290ac2f555eabca9e31180cf38e91f9e7e2761' in commit_hashes
    assert '71535a31f0b598a5d5fcebda7146ebc01def783a' in commit_hashes
    assert '57dbd017d1a744b949e7ca0b1c1a3b3dd4c1cbc1' in commit_hashes
    assert '866e997a9e44cb4ddd9e00efe49361420aff2559' in commit_hashes


def test_only_releases():
    lc = list(RepositoryMining('test-repos/git-8/',
                               only_releases=True).traverse_commits())

    assert len(lc) == 3
    assert '6bb9e2c6a8080e6b5b34e6e316c894b2ddbf7fcd' == lc[0].hash
    assert '4638730126d40716e230c2040751a13153fb1556' == lc[1].hash
    assert '627e1ad917a188a861c9fedf6e5858b79edbe439' == lc[2].hash


def test_only_releases_wo_releases():
    lc = list(RepositoryMining('test-repos/git-1/',
                               only_releases=True).traverse_commits())

    assert len(lc) == 0