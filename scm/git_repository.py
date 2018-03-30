from typing import List
from git import Git, Repo, Diff, GitCommandError
from git.objects.util import tzoffset

from domain.change_set import ChangeSet
from domain.commit import Commit
from domain.developer import Developer
import os
from domain.modification_type import ModificationType
from threading import Lock
from datetime import datetime


class GitRepository:
    def __init__(self, path: str, first_parent_only: str = False):
        """
        Init the Git Repository
        :param path: path to the repository
        :param first_parent_only: True if it has to analyze only the non merge commits
        """
        self.path = path
        self.first_parent_only = first_parent_only
        self.main_branch = None
        self.lock = Lock()

    def __open_git(self) -> Git:
        self.__open_repository()
        return Git(self.path)

    def __open_repository(self) -> Repo:
        repo = Repo(self.path)
        if self.main_branch is None:
            self.__discover_main_branch(repo)
        return repo

    def __discover_main_branch(self, repo):
        self.main_branch = repo.active_branch.name

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
            committer_date = self.__get_time(commit.committed_date, commit.committer_tz_offset)
            change_sets.append(ChangeSet(commit.hexsha, committer_date))
        return change_sets


    def __get_time(self, timestamp, tz_offset):
        try:
            dt = datetime.fromtimestamp(timestamp).astimezone(tzoffset(tz_offset))
        except ValueError:
            dt = datetime.fromtimestamp(timestamp).astimezone(tzoffset(0, 'UTC'))
            print('Error in retrieving dates information')
        return dt

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

        author_date = self.__get_time(commit.authored_date, author_timezone)
        committer_date = self.__get_time(commit.committed_date, author_timezone)

        merge = True if len(commit.parents) > 1 else False

        parents = []
        for p in commit.parents:
            parents.append(p.hexsha)

        branches = self.__get_branches(git, commit_hash)
        is_in_main_branch = self.main_branch in branches

        the_commit = Commit(commit_hash, author, committer, author_date, committer_date, author_timezone,
                            committer_timezone, msg,
                            parents, merge, branches,is_in_main_branch)

        if len(parents) > 0:
            parent = repo.commit(parents[0])
            diff_index = parent.diff(commit, create_patch=True)
        else:
            parent = repo.tree('4b825dc642cb6eb9a060e54bf8d69288fbee4904')
            diff_index = parent.diff(commit.tree, create_patch=True)

        self.__parse_diff(diff_index, the_commit)

        return the_commit

    def __parse_diff(self, diff_index, the_commit):
        for d in diff_index:
            old_path = d.a_path
            new_path = d.b_path
            change_type = self.__from_change_to_modification_type(d)
            sc = ''
            diff_text = ''
            try:
                sc = d.b_blob.data_stream.read().decode('utf-8')
                diff_text = d.diff.decode('utf-8')
            except (UnicodeDecodeError, AttributeError, ValueError):
                print('Couldn\'t load all the information regarding commit {}'.format(the_commit.hash))

            the_commit.add_modifications(old_path, new_path, change_type, diff_text, sc)

    def __get_branches(self, git: Git, commit_hash: str):
        branches = set()
        for branch in set(git.branch('--contains', commit_hash).split('\n')):
            branches.add(branch.strip().replace('* ', ''))
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
            self.__delete_tmp_branch()
            git.checkout('-f', hash, b='_PD')

    def __delete_tmp_branch(self):
        repo = self.__open_repository()
        try:
            repo.delete_head('_PD')
        except GitCommandError:
            print("Branch _PD not found")

    def files(self):
        all = []
        for path, subdirs, files in os.walk(self.path):
            if '.git' in path:
                continue
            for name in files:
                all.append(os.path.join(path, name))
        return all

    def reset(self):
        with self.lock:
            git = self.__open_git()
            git.checkout('-f', self.main_branch)
            self.__delete_tmp_branch()

    def total_commits(self) -> int:
        return len(self.get_change_sets())

    def get_commit_from_tag(self, tag: str) -> Commit:
        repo = self.__open_repository()
        try:
            selected_tag = repo.tags[tag]
            return self.get_commit(selected_tag.commit.hexsha)
        except (IndexError, AttributeError):
            print('Tag {} not found'.format(tag))
            raise