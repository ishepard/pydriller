from git import Git, Repo, GitCommandError
from domain.change_set import ChangeSet

class GitRepository:
    def __init__(self, path: str, first_parent_only: str = False):
        self.path = path
        self.first_parent_only = first_parent_only

    def __open_repository(self):
        return Git(self.path)

    def get_head(self):
        repo = Repo(self.path)
        head_commit = repo.head.commit
        return ChangeSet(head_commit.hexsha, head_commit.committed_datetime)

    def get_change_sets(self):
        return self.__get_all_commits()

    def __get_all_commits(self):
        repo = Repo(self.path)
        commit_list = list(repo.iter_commits())

        change_sets = []
        for commit in commit_list:
            change_sets.append(ChangeSet(commit.hexsha, commit.committed_datetime))
        return change_sets