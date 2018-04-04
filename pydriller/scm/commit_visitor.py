import abc
from pydriller.scm.git_repository import GitRepository
from pydriller.domain.commit import Commit
from pydriller.scm.persistence_mechanism import PersistenceMechanism


class CommitVisitor(abc.ABC):
    @abc.abstractmethod
    def process(self, repo: GitRepository, commit: Commit, writer: PersistenceMechanism):
        pass