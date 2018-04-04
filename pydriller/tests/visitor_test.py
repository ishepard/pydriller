from pydriller.domain.commit import Commit
from pydriller.scm.commit_visitor import CommitVisitor
from pydriller.scm.git_repository import GitRepository
from pydriller.scm.persistence_mechanism import PersistenceMechanism


class VisitorTest(CommitVisitor):
    def __init__(self):
        self.list_commits = []

    def process(self, repo: GitRepository, commit: Commit, writer: PersistenceMechanism):
        self.list_commits.append(commit)