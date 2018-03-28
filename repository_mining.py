from scm.commit_visitor import CommitVisitor
from scm.git_repository import GitRepository
from domain.commit import Commit
from domain.change_set import ChangeSet
from scm.commit_visitor import CommitVisitor


class RepositoryMining:
    def __init__(self, path_to_repo: str, visitor: CommitVisitor):
        """
        Init a repository mining.
        :param path_to_repo: absolute path to the repository you have to mine
        :param visitor: CommitVisitor that will visit all the specified commits
        """
        self.git_repo = GitRepository(path_to_repo)
        self.visitor = visitor

    def mine(self):
        """
        Starts the mining.
        """
        self.__process_repo()

    def __process_repo(self):
        print('Git repository in {}'.format(self.git_repo.path))
        all_cs = self.git_repo.get_change_sets()

        for cs in all_cs:
            self.__process_cs(cs)

    def __process_cs(self, cs: ChangeSet):
        commit = self.git_repo.get_commit(cs.id)
        print('Commit #{} in {} from {} with {} modifications'
              .format(commit.hash, commit.date, commit.author.name, len(commit.modifications)))

        self.visitor.process(self.git_repo, commit, None)

