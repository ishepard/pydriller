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

import pytest

from pydriller.repository_mining import RepositoryMining


@pytest.yield_fixture(scope="function")
def lc(request):
    reversed = request.param
    yield list(RepositoryMining('test-repos/git-4',
                                reversed_order=reversed).traverse_commits())


@pytest.mark.parametrize('lc', [False], indirect=True)
def test_should_visit_ascendent_order(lc):
    assert len(lc) == 3
    assert lc[0].hash == 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5'
    assert lc[1].hash == '375de7a8275ecdc0b28dc8de2568f47241f443e9'
    assert lc[2].hash == 'b8c2be250786975f1c6f47e96922096f1bb25e39'


@pytest.mark.parametrize('lc', [True], indirect=True)
def test_should_visit_descendent_order(lc):
    assert len(lc) == 3
    assert lc[2].hash == 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5'
    assert lc[1].hash == '375de7a8275ecdc0b28dc8de2568f47241f443e9'
    assert lc[0].hash == 'b8c2be250786975f1c6f47e96922096f1bb25e39'
