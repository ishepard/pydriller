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

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

import pytest

from pydriller.git_repository import GitRepository


@pytest.yield_fixture(scope="module")
def resource():
    yield GitRepository('test-repos/git-1/')


def test_equal(resource):
    c1 = resource.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2')
    c2 = resource.get_commit(c1.parents[0])
    c3 = resource.get_commit('a4ece0762e797d2e2dcbd471115108dd6e05ff58')

    assert c1.parents[0] == 'a4ece0762e797d2e2dcbd471115108dd6e05ff58'
    assert c2 == c3
    assert c1 != c3

def test_filename():
    m1 = Modification('/Users/dspadini/pydriller/myfile.py', "/Users/dspadini/pydriller/mynewfile.py", ModificationType.ADD, [], '')
    m3 = Modification('/Users/dspadini/pydriller/myfile.py', "/Users/dspadini/pydriller/mynewfile.py",
                      ModificationType.ADD, [], '')
    m2 = Modification('/Users/dspadini/pydriller/myfile.py', None,
                      ModificationType.ADD, [], '')

    assert m1.filename == 'mynewfile.py'
    assert m2.filename == 'myfile.py'
    assert m1 != m2
    assert m1 == m3