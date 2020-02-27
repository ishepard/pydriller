"""
Configuration module.
"""

import logging
from datetime import datetime

import pytz
from gitdb.exc import BadName

from pydriller.domain.commit import Commit

logger = logging.getLogger(__name__)


class Conf:
    """
    Configuration class. This class holds all the possible configurations of
    the mining process (i.e., starting and ending dates, branches, etc.)
    It's also responsible for checking whether the filters are correct (i.e.,
    the user did not specify 2 starting commits).
    """

    def __init__(self, options):
        # insert all the configurations in a local dictionary
        self._options = {}
        for key, val in options.items():
            self._options[key] = val

        self._sanity_check_repos(self.get('path_to_repo'))
        if isinstance(self.get('path_to_repo'), str):
            self.set_value('path_to_repos', [self.get('path_to_repo')])
        else:
            self.set_value('path_to_repos', self.get('path_to_repo'))

    def set_value(self, key, value):
        """
        Save the value of a configuration.

        :param key: configuration (i.e., start date)
        :param value: value
        """
        self._options[key] = value

    def get(self, key):
        """
        Return the value of the configuration.

        :param key: configuration name
        :return: value of the configuration, None if not present
        """
        return self._options.get(key, None)

    @staticmethod
    def _sanity_check_repos(path_to_repo):
        """
        Checks if repo is of type str or list.

        @param path_to_repo: path to the repo as provided by the user.
        @return:
        """
        if not isinstance(path_to_repo, str) and \
                not isinstance(path_to_repo, list):
            raise Exception("The path to the repo has to be of type "
                            "'string' or 'list of strings'!")

    def sanity_check_filters(self):
        """
        Check if the values passed by the user are correct.

        """
        self.check_starting_commit()
        self.check_ending_commit()
        self._check_timezones()

        if self.get("from_commit") and self.get("to_commit") and self.get(
                "from_commit") == self.get("to_commit"):
            logger.warning("You should not point from_commit and "
                           "to_commit to the same commit, but use the "
                           "'single' filter instead.")
            single = self.get("to_commit")
            self.set_value("from_commit", None)
            self.set_value("to_commit", None)
            self.set_value("single", single)

        self._check_correct_filters_order()

        if self.get('single') is not None:
            if any([self.get('since'),
                    self.get('to'),
                    self.get('from_commit'),
                    self.get('to_commit'),
                    self.get('from_tag'),
                    self.get('to_tag')]):
                raise Exception('You can not specify a single commit with '
                                'other filters')
            try:
                self.set_value('single', self.get("git_repo").get_commit(
                    self.get('single')).hash)
            except BadName:
                raise Exception("The commit {} defined in "
                                "the 'single' filtered does "
                                "not exist".format(self.get('single')))

    def _check_correct_filters_order(self):
        """
        from_commit should come before to_commit when analyzing a repository
        with the default settings, while they should be swapped when
        analyzing the repository with reversed_order=True
        """
        if self.get('from_commit') and self.get('to_commit'):
            chronological_order = self._is_commit_before(
                self.get('git_repo').get_commit(self.get('from_commit')),
                self.get('git_repo').get_commit(self.get('to_commit')))

            if self.get('reversed_order') and chronological_order:
                self._swap_commit_fiters()
            elif not self.get('reversed_order') and not chronological_order:
                self._swap_commit_fiters()

    def _swap_commit_fiters(self):
        # reverse from and to commit
        from_commit = self.get('from_commit')
        to_commit = self.get('to_commit')
        self.set_value('from_commit', to_commit)
        self.set_value('to_commit', from_commit)

    @staticmethod
    def _is_commit_before(commit_before, commit_after):
        return commit_before.committer_date < commit_after.committer_date

    def check_starting_commit(self):
        """
        Get the starting commit from the 'since', 'from_commit' or 'from_tag'
        filter.
        """
        if not self.only_one_filter([self.get('since'),
                                     self.get('from_commit'),
                                     self.get('from_tag')]):
            raise Exception('You can only specify one between since, '
                            'from_tag and from_commit')
        if self.get('from_tag') is not None:
            self.set_value('from_commit', self.get(
                "git_repo").get_commit_from_tag(self.get('from_tag')).hash)
        if self.get('from_commit'):
            try:
                self.set_value('from_commit', self.get("git_repo").get_commit(
                    self.get('from_commit')).hash)
            except BadName:
                raise Exception("The commit {} defined in the 'from_tag' "
                                "or 'from_commit' filter does "
                                "not exist".format(self.get('single')))

    def check_ending_commit(self):
        """
        Get the ending commit from the 'to', 'to_commit' or 'to_tag' filter.
        """
        if not self.only_one_filter([self.get('to'),
                                     self.get('to_commit'),
                                     self.get('to_tag')]):
            raise Exception('You can only specify one between since, '
                            'from_tag and from_commit')
        if self.get('to_tag') is not None:
            self.set_value('to_commit', self.get(
                "git_repo").get_commit_from_tag(self.get('to_tag')).hash)
        if self.get('to_commit'):
            try:
                self.set_value('to_commit', self.get("git_repo").get_commit(
                    self.get('to_commit')).hash)
            except BadName as e:
                raise Exception("The commit {} defined in the 'to_tag' "
                                "or 'to_commit' filter does "
                                "not exist".format(self.get('single')))

    @staticmethod
    def only_one_filter(arr):
        """
        Return true if in 'arr' there is at most 1 filter to True.

        :param arr: iterable object
        :return:
        """
        return len([x for x in arr if x is not None]) <= 1

    def is_commit_filtered(self, commit: Commit):
        # pylint: disable=too-many-branches,too-many-return-statements
        """
        Check if commit has to be filtered according to the filters provided
        by the user.

        :param Commit commit: Commit to check
        :return:
        """
        if self.get('single') is not None and \
                commit.hash != self.get('single'):
            logger.debug('Commit filtered because is not '
                         'the defined in single')
            return True
        if (self.get('since') is not None and
            commit.committer_date < self.get('since')) or \
                (self.get('to') is not None and
                 commit.committer_date > self.get('to')):
            return True
        if self.get('from_commit') is not None and \
                self.get('from_commit') == commit.hash:
            self.set_value('from_commit_started', True)
            return False
        if self.get('from_commit') is not None and \
                self.get('from_commit') != commit.hash and \
                self.get('from_commit_started') is None:
            return True
        if self.get('to_commit') is not None and \
                self.get('to_commit') != commit.hash and \
                self.get('to_commit_reached') is not None:
            return True
        if self.get('to_commit') is not None and \
                self.get('to_commit') == commit.hash:
            self.set_value('to_commit_reached', True)
            return False
        if self.get('only_modifications_with_file_types') is not None:
            if not self._has_modification_with_file_type(commit):
                logger.debug('Commit filtered for modification types')
                return True
        if self.get('only_no_merge') is True and commit.merge is True:
            logger.debug('Commit filtered for no merge')
            return True
        if self.get('only_authors') is not None and \
                commit.author.name not in self.get('only_authors'):
            logger.debug("Commit filtered for author")
            return True
        if self.get('only_commits') is not None and \
                commit.hash not in self.get('only_commits'):
            logger.debug("Commit filtered because it is not one of the "
                         "specified commits")
            return True
        if self.get('filepath_commits') is not None and \
                commit.hash not in self.get('filepath_commits'):
            logger.debug("Commit filtered because it did not modify the "
                         "specified file")
            return True
        if self.get('tagged_commits') is not None and \
                commit.hash not in self.get('tagged_commits'):
            logger.debug("Commit filtered because it is not tagged")
            return True
        return False

    def _has_modification_with_file_type(self, commit):
        for mod in commit.modifications:
            if mod.filename.endswith(
                    tuple(self.get('only_modifications_with_file_types'))):
                return True
        return False

    def _check_timezones(self):
        if self.get('since') is not None:
            self.set_value('since', self._replace_timezone(self.get('since')))
        if self.get('to') is not None:
            self.set_value('to', self._replace_timezone(self.get('to')))

    @staticmethod
    def _replace_timezone(dt: datetime):
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            dt = dt.replace(tzinfo=pytz.utc)
        return dt
