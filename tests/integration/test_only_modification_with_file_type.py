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

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

from pydriller.repository_mining import RepositoryMining


def test_mod_with_file_types():
    lc = list(RepositoryMining('test-repos/git-7/', only_modifications_with_file_types=['.java']).traverse_commits())

    assert len(lc) == 2
    assert lc[0].hash == '5adbb71167e79ab6b974827e74c9da4d81977655'
    assert lc[1].hash == '0577bec2387ee131e1ccf336adcc172224d3f6f9'
