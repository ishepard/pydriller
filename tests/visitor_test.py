from domain.commit import Commit
from scm.commit_visitor import CommitVisitor
from scm.git_repository import GitRepository
from scm.persistence_mechanism import PersistenceMechanism


class VisitorTest(CommitVisitor):
    def __init__(self):
        self.list_commits = []

    def process(self, repo: GitRepository, commit: Commit, writer: PersistenceMechanism):
        self.list_commits.append(commit)