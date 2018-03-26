from git import Git, Repo, Blob, Diff
from domain.change_set import ChangeSet
from domain.commit import Commit
from domain.developer import Developer
import os
from pprint import pprint
from domain.modification_type import ModificationType
from threading import Lock
from utils.file_utils import FileUtils

class GitRepository:
    def __init__(self, path: str, first_parent_only: str = False):
        self.path = path
        self.first_parent_only = first_parent_only
        self.lock = Lock()

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
        msg = commit.message.strip()
        commit_hash = commit.hexsha

        if len(commit.parents) > 0:
            parent = commit.parents[0].hexsha
        else:
            parent = ''

        author_date = commit.authored_datetime
        committer_date = commit.committed_datetime
        merge = True if len(commit.parents) > 1 else False

        # TODO: branches is not correct, there should be a better way to do it
        branches = self.__get_branches(git, commit_hash)

        # TODO: calculate main branch
        main_branch = False

        the_commit = Commit(commit_hash, author, committer, author_date, committer_date, msg, parent, merge, branches)

        # TODO: if commit does not have a parent, this will fail
        diff_index = commit.diff(commit_hash + '~1')

        # TODO: diff is empty, to investigate why
        for d in diff_index:
            # print("A blob:\n{}".format(d.a_blob.data_stream.read().decode('utf-8')))
            # print("B blob:\n{}".format(d.b_blob.data_stream.read().decode('utf-8')))
            old_path = d.a_path
            new_path = d.b_path
            diff_text = d.diff
            # pprint(vars(Diff))
            # pprint(d.diff)
            change_type = self.__from_change_to_modification_type(d.change_type)
            sc = d.b_blob.data_stream.read().decode('utf-8')

            the_commit.add_modifications(old_path, new_path, change_type, diff_text, sc)

        return the_commit

    def __get_branches(self, git: Git, commit_hash: str):
        branches = list(git.branch('--contains', commit_hash).split('\n'))
        return branches

    def __from_change_to_modification_type(self, type: str):
        if type == 'M':
            return ModificationType.MODIFY
        elif type == 'A':
            return ModificationType.ADD
        elif type == 'D':
            return ModificationType.DELETE
        elif type == 'R':
            return ModificationType.RENAME

    def checkout(self, hash: str):
        with self.lock:
            git = self.__open_repository()
            git.checkout(hash)

    def files(self):
        all = []
        for path, subdirs, files in os.walk(self.path):
            for name in files:
                all.append(os.path.join(path, name))
        return all

    
