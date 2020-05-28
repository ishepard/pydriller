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

from pydriller.repository_mining import RepositoryMining
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def test_between_revisions():
    from_tag = 'tag1'
    to_tag = 'tag3'

    lc = list(RepositoryMining('test-repos/tags',
                               from_tag=from_tag,
                               to_tag=to_tag).traverse_commits())

    assert len(lc) == 5
    assert '6bb9e2c6a8080e6b5b34e6e316c894b2ddbf7fcd' == lc[0].hash
    assert 'f1a90b8d7b151ceefd3e3dfc0dc1d0e12b5f48d0' == lc[1].hash
    assert '4638730126d40716e230c2040751a13153fb1556' == lc[2].hash
    assert 'a26f1438bd85d6b22497c0e5dae003812becd0bc' == lc[3].hash
    assert '627e1ad917a188a861c9fedf6e5858b79edbe439' == lc[4].hash


def test_multiple_repos_with_tags():
    from_tag = 'tag2'
    to_tag = 'tag3'
    repos = [
        'test-repos/tags',
        'test-repos/tags',
        'test-repos/tags'
    ]
    lc = list(RepositoryMining(path_to_repo=repos,
                               from_tag=from_tag,
                               to_tag=to_tag).traverse_commits())
    assert len(lc) == 9
