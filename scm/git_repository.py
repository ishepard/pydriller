from git import Git, Repo, GitCommandError
from domain.change_set import ChangeSet
from domain.commit import Commit
from domain.developer import Developer
from datetime import datetime

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

    def get_commit(self, commit_id: str):
        git = self.__open_repository()
        repo = Repo(self.path)
        commit = repo.commit(commit_id)

        author = Developer(commit.author.name, commit.author.email)
        committer = Developer(commit.committer.name, commit.committer.email)
        author_timezone = commit.author_tz_offset
        committer_timezone = commit.committer_tz_offset
        msg = commit.message
        commit_hash = commit.hexsha

        if len(commit.parents) > 0:
            parent = commit.parents[0]
        else:
            parent = ''

        author_date = commit.authored_datetime
        committer_date = commit.committed_datetime
        merge = False if len(commit.parents) > 1 else True

        # TODO: branches is not correct, there should be a better way to do it
        branches = self.__get_branches(git, commit_hash)

        # TODO: calculate main branch
        main_branch = False

        the_commit = Commit(commit_hash, author, committer, author_date, committer_date, msg, parent, merge, branches)
        return the_commit

    def __get_branches(self, git: Git, commit_hash: str):
        branches = list(git.branch('--contains', commit_hash).split('\n'))
        return branches
