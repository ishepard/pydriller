import abc
from scm.scm_repository import SCMRepository
from scm.persistence_mechanism import PersistenceMechanism


class CommitVisitor(abc.ABC):
    @abc.abstractmethod
    def process(self, repo: SCMRepository, writer: PersistenceMechanism):
        pass