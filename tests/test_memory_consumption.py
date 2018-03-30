import os
import psutil
import sys

from domain.commit import Commit
from repository_mining import RepositoryMining
from scm.commit_visitor import CommitVisitor
from scm.git_repository import GitRepository
from scm.persistence_mechanism import PersistenceMechanism
from datetime import datetime


def test_memory():
    if 'TRAVIS' not in os.environ:
        return

    p = psutil.Process()
    mv = MemoryVisitor(p)

    start = datetime.now()
    RepositoryMining('test-repos/rails', mv,
                     from_commit='977b4be208c2c54eeaaf7b46953174ef402f49d4',
                     to_commit='ede505592cfab0212e53ca8ad1c38026a7b5d042').mine()
    end = datetime.now()

    diff = end - start
    print('Max memory {} Mb'.format(mv.maxMemory))
    print('Min memory {} Mb'.format(mv.minMemory))
    print('Min memory {} Mb'.format(', '.join(map(str, mv.all))))
    print('Time {}'.format(diff.min))


class MemoryVisitor(CommitVisitor):
    def __init__(self, p):
        self.p = p
        self.maxMemory = -sys.maxsize
        self.minMemory = sys.maxsize
        self.numberOfCommits = 0
        self.all = []

    def process(self, repo: GitRepository, commit: Commit, writer: PersistenceMechanism):
        memory = self.p.memory_info().vms / (2 ** 20)

        if memory > self.maxMemory: self.maxMemory = memory
        if memory < self.minMemory: self.minMemory = memory

        self.all.append(memory)

        self.numberOfCommits += 1