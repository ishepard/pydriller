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

from pydriller.repository import Repository

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

to_zone = timezone(timedelta(hours=-4))
dt1 = datetime(2016, 10, 8, 17, 0, 0, tzinfo=to_zone)
dt2 = datetime(2016, 10, 8, 17, 59, 0, tzinfo=to_zone)


def test_between_dates():
    list_commits = list(Repository('test-repos/different_files',
                                   since=dt1,
                                   to=dt2).traverse_commits())

    assert len(list_commits) == 2
    assert list_commits[0].hash == 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5'
    assert list_commits[1].hash == '375de7a8275ecdc0b28dc8de2568f47241f443e9'


def test_between_dates_without_timezone():
    dt1 = datetime(2016, 10, 8, 21, 0, 0)
    dt2 = datetime(2016, 10, 8, 21, 59, 0)
    list_commits = list(Repository('test-repos/different_files',
                                   since=dt1,
                                   to=dt2).traverse_commits())

    assert len(list_commits) == 2
    assert list_commits[0].hash == 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5'
    assert list_commits[1].hash == '375de7a8275ecdc0b28dc8de2568f47241f443e9'


def test_between_dates_reversed():
    lc = list(Repository('test-repos/different_files',
                         since=dt1,
                         to=dt2,
                         order='reverse').traverse_commits())

    assert len(lc) == 2
    assert lc[0].hash == '375de7a8275ecdc0b28dc8de2568f47241f443e9'
    assert lc[1].hash == 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5'
