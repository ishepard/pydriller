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


def test_should_visit_ascendent_order():
    lc = list(RepositoryMining('test-repos/small_repo',
                               reversed_order=False).traverse_commits())
    assert len(lc) == 5
    assert lc[0].hash == 'a88c84ddf42066611e76e6cb690144e5357d132c'
    assert lc[1].hash == '6411e3096dd2070438a17b225f44475136e54e3a'
    assert lc[2].hash == '09f6182cef737db02a085e1d018963c7a29bde5a'
    assert lc[3].hash == '1f99848edadfffa903b8ba1286a935f1b92b2845'
    assert lc[4].hash == 'da39b1326dbc2edfe518b90672734a08f3c13458'


def test_should_visit_descendent_order():
    lc = list(RepositoryMining('test-repos/small_repo',
                               reversed_order=True).traverse_commits())
    assert len(lc) == 5
    assert lc[0].hash == 'da39b1326dbc2edfe518b90672734a08f3c13458'
    assert lc[1].hash == '1f99848edadfffa903b8ba1286a935f1b92b2845'
    assert lc[2].hash == '09f6182cef737db02a085e1d018963c7a29bde5a'
    assert lc[3].hash == '6411e3096dd2070438a17b225f44475136e54e3a'
    assert lc[4].hash == 'a88c84ddf42066611e76e6cb690144e5357d132c'


def test_should_visit_descendent_order_with_filters():
    lc = list(RepositoryMining('test-repos/small_repo',
                               from_commit='1f99848edadfffa903b8ba1286a935f1b92b2845',
                               to_commit='6411e3096dd2070438a17b225f44475136e54e3a',
                               reversed_order=True).traverse_commits())
    assert len(lc) == 3
    assert lc[0].hash == '1f99848edadfffa903b8ba1286a935f1b92b2845'
    assert lc[1].hash == '09f6182cef737db02a085e1d018963c7a29bde5a'
    assert lc[2].hash == '6411e3096dd2070438a17b225f44475136e54e3a'


def test_should_visit_descendent_order_with_filters_reversed():
    lc = list(RepositoryMining('test-repos/small_repo',
                               from_commit='6411e3096dd2070438a17b225f44475136e54e3a',
                               to_commit='1f99848edadfffa903b8ba1286a935f1b92b2845',
                               reversed_order=True).traverse_commits())
    assert len(lc) == 3
    assert lc[0].hash == '1f99848edadfffa903b8ba1286a935f1b92b2845'
    assert lc[1].hash == '09f6182cef737db02a085e1d018963c7a29bde5a'
    assert lc[2].hash == '6411e3096dd2070438a17b225f44475136e54e3a'