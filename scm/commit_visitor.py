import abc
from scm.git_repository import GitRepository
from domain.commit import Commit
from scm.persistence_mechanism import PersistenceMechanism


class CommitVisitor(abc.ABC):
    @abc.abstractmethod
    def process(self, repo: GitRepository, commit: Commit, writer: PersistenceMechanism):
        pass