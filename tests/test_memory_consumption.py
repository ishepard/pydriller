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

import os
import psutil
if 'TRAVIS' in os.environ:
    import logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
from pydriller.repository_mining import RepositoryMining
from datetime import datetime, timezone


def test_memory():
    if 'TRAVIS' not in os.environ:
        return

    p = psutil.Process(os.getpid())
    number_of_commits = 0
    all_commits = []

    dt1 = datetime(2015, 1, 1)
    dt2 = datetime(2016, 1, 1)

    start = datetime.now()
    for _ in RepositoryMining('test-repos/hadoop',
                              since=dt1,
                              to=dt2).traverse_commits():
        memory = p.memory_info()[0] / (2 ** 20)
        all_commits.append(memory)
        number_of_commits += 1

    end = datetime.now()

    diff = end - start
    logging.info('Max memory {} Mb'.format(max(all_commits)))
    logging.info('Min memory {} Mb'.format(min(all_commits)))
    logging.info('All: {}'.format(', '.join(map(str, all_commits))))
    logging.info('Time {}:{}:{}'.format(diff.seconds//3600, (diff.seconds % 3600) // 60, diff.seconds % 60))
    logging.info('Commits per second: {}'.format(len(all_commits) / diff.seconds))