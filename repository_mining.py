from typing import List
from scm.git_repository import GitRepository
from domain.change_set import ChangeSet
from scm.commit_visitor import CommitVisitor
from datetime import datetime


class RepositoryMining:
    def __init__(self, path_to_repo: str, visitor: CommitVisitor, single: str = None, since: datetime = None,
                 to: datetime = None, from_commit: str = None, to_commit: str = None, from_tag: str = None,
                 to_tag: str = None, reversed_order: bool = False):
        """
        Init a repository mining.
        :param str path_to_repo: absolute path to the repository you have to mine
        :param CommitVisitor visitor: CommitVisitor that will visit all the specified commits
        :param str single: hash of a single commit to analyze
        :param datetime since: starting date
        :param datetime to: ending date
        :param str from_commit: starting commit (only if `since` is None)
        :param str to_commit: ending commit (only if `to` is None)
        :param str from_tag: starting the analysis from specified tag (only if `since` and `from_commit` are None)
        :param str to_tag: ending the analysis from specified tag (only if `to` and `to_commit` are None)
        """
        self.git_repo = GitRepository(path_to_repo)
        self.visitor = visitor
        self.single = single
        self.since = since
        self.to = to
        self.reversed_order = reversed_order

        if from_commit is not None:
            if since is not None:
                raise Exception('You can not specify both <since date> and <from commit>')
            self.since = self.git_repo.get_commit(from_commit).date

        if to_commit is not None:
            if to is not None:
                raise Exception('You can not specify both <to date> and <to commit>')
            self.to = self.git_repo.get_commit(to_commit).date

        if from_tag is not None:
            if since is not None or from_commit is not None:
                raise Exception('You can not specify <since date> or <from commit> when using <from tag>')
            self.since = self.git_repo.get_commit_from_tag(from_tag).date

        if to_tag is not None:
            if to is not None or to_commit is not None:
                raise Exception('You can not specify <to date> or <to commit> when using <to tag>')
            self.to = self.git_repo.get_commit_from_tag(to_tag).date

    def mine(self):
        """
        Starts the mining.
        """
        self.__process_repo()

    def __process_repo(self):
        print('Git repository in {}'.format(self.git_repo.path))
        all_cs = self.__apply_filters(self.git_repo.get_change_sets())

        if not self.reversed_order:
            all_cs.reverse()

        for cs in all_cs:
            self.__process_cs(cs)

    def __process_cs(self, cs: ChangeSet):
        commit = self.git_repo.get_commit(cs.id)
        print('Commit #{} in {} from {} with {} modifications'
              .format(commit.hash, commit.date, commit.author.name, len(commit.modifications)))

        self.visitor.process(self.git_repo, commit, None)

    def __apply_filters(self, all_cs: List[ChangeSet]) -> List[ChangeSet]:
        res = []

        if self.__all_filters_are_none():
            return all_cs

        for cs in all_cs:
            if self.single is not None and cs.id == self.single:
                return [cs]
            if self.since is None or self.since <= cs.date:
                if self.to is None or cs.date <= self.to:
                    res.append(cs)
                    continue
        return res

    def __all_filters_are_none(self):
        return self.since is None and self.to is None

