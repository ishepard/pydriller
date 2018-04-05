import os
import psutil
if 'TRAVIS' in os.environ:
    import logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

from pydriller.domain.commit import Commit
from pydriller.repository_mining import RepositoryMining
from pydriller.git_repository import GitRepository
from datetime import datetime


def test_memory():
    if 'TRAVIS' not in os.environ:
        return

    p = psutil.Process(os.getpid())
    number_of_commits = 0
    all_commits = []

    start = datetime.now()
    for _ in RepositoryMining('test-repos/rails',
                              from_commit='977b4be208c2c54eeaaf7b46953174ef402f49d4',
                              to_commit='ede505592cfab0212e53ca8ad1c38026a7b5d042').traverse_commits():
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