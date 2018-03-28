from typing import List

from git import Git, Repo, Diff
from domain.change_set import ChangeSet
from domain.commit import Commit
from domain.developer import Developer
import os
from pprint import pprint
from domain.modification_type import ModificationType
from threading import Lock


class GitRepository:
    def __init__(self, path: str, first_parent_only: str = False):
        """
        Init the Git Repository
        :param path: path to the repository
        :param first_parent_only: True if it has to analyze only the non merge commits
        """
        self.path = path
        self.first_parent_only = first_parent_only
        self.lock = Lock()

    def __open_git(self) -> Git:
        return Git(self.path)

    def __open_repository(self) -> Repo:
        return Repo(self.path)

    def get_head(self) -> ChangeSet:
        """
        Get the head commit.
        :return: ChangeSet of the head commit
        """
        repo = self.__open_repository()
        head_commit = repo.head.commit
        return ChangeSet(head_commit.hexsha, head_commit.committed_datetime)

    def get_change_sets(self) -> List[ChangeSet]:
        return self.__get_all_commits()

    def __get_all_commits(self) -> List[ChangeSet]:
        repo = self.__open_repository()
        commit_list = list(repo.iter_commits())

        change_sets = []
        for commit in commit_list:
            change_sets.append(ChangeSet(commit.hexsha, commit.committed_datetime))
        return change_sets

    def get_commit(self, commit_id: str) -> Commit:
        """
        Get the commit.
        :param commit_id: hash of the commit to analyze
        :return: Commit
        """
        git = self.__open_git()
        repo = self.__open_repository()
        commit = repo.commit(commit_id)

        author = Developer(commit.author.name, commit.author.email)
        committer = Developer(commit.committer.name, commit.committer.email)
        author_timezone = commit.author_tz_offset
        committer_timezone = commit.committer_tz_offset
        msg = commit.message.strip()
        commit_hash = commit.hexsha

        author_date = commit.authored_datetime
        committer_date = commit.committed_datetime
        merge = True if len(commit.parents) > 1 else False

        # TODO: branches is not correct, there should be a better way to do it
        branches = self.__get_branches(git, commit_hash)

        # TODO: calculate main branch
        main_branch = False
        if len(commit.parents) > 0:
            parent = repo.commit(commit.parents[0].hexsha)
            the_commit = Commit(commit_hash, author, committer, author_date, committer_date, msg, parent.hexsha, merge, branches)
            diff_index = parent.diff(commit, create_patch=True)
        else:
            the_commit = Commit(commit_hash, author, committer, author_date, committer_date, msg, '', merge,
                                branches)
            parent = repo.tree('4b825dc642cb6eb9a060e54bf8d69288fbee4904')
            diff_index = parent.diff(commit.tree, create_patch=True)

        self.__parse_diff(diff_index, the_commit)

        return the_commit

    def __parse_diff(self, diff_index, the_commit):
        for d in diff_index:
            old_path = d.a_path
            new_path = d.b_path
            diff_text = d.diff.decode('utf-8')
            change_type = self.__from_change_to_modification_type(d)
            sc = d.b_blob.data_stream.read().decode('utf-8')
            # print("Sc is {}".format(sc))
            # print("Diff is {}".format(diff_text))
            # print("Change type is {}".format(change_type))
            # print("Old path {}".format(old_path))
            # print("New path {}".format(new_path))
            the_commit.add_modifications(old_path, new_path, change_type, diff_text, sc)

    def __get_branches(self, git: Git, commit_hash: str):
        branches = set(git.branch('--contains', commit_hash).split('\n'))
        return branches

    def __from_change_to_modification_type(self, d: Diff):
        if d.new_file:
            return ModificationType.ADD
        elif d.deleted_file:
            return ModificationType.DELETE
        elif d.renamed_file:
            return ModificationType.RENAME
        elif d.a_blob and d.b_blob and d.a_blob != d.b_blob:
            return ModificationType.MODIFY

    def checkout(self, hash: str):
        with self.lock:
            git = self.__open_git()
            git.checkout(hash)

    def files(self):
        all = []
        for path, subdirs, files in os.walk(self.path):
            for name in files:
                all.append(os.path.join(path, name))
        return all

    def reset(self):
        with self.lock:
            git = self.__open_git()
            git.reset()

    def total_commits(self) -> int:
        return len(self.get_change_sets())

    def get_commit_from_tag(self, tag: str) -> str:
        repo = self.__open_repository()
        try:
            selected_tag = repo.tags[tag]
            return selected_tag.commit.hexsha
        except (IndexError, AttributeError):
            print('Tag {} not found'.format(tag))
            raise


