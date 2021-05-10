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
        if not isinstance(path_to_repo, str) and not isinstance(path_to_repo, list):
            raise Exception("The path to the repo has to be of type 'string' or 'list of strings'!")

    def _check_only_one_from_commit(self):
        if not self.only_one_filter([self.get('since'),
                                     self.get('from_commit'),
                                     self.get('from_tag')]):
            raise Exception('You can only specify one filter between since, from_tag and from_commit')

    def _check_only_one_to_commit(self):
        if not self.only_one_filter([self.get('to'),
                                     self.get('to_commit'),
                                     self.get('to_tag')]):
            raise Exception('You can only specify one between since, from_tag and from_commit')

    def sanity_check_filters(self):
        """
        Check if the values passed by the user are correct.

        """
        self._check_correct_filters_order()
        self._check_only_one_from_commit()
        self._check_only_one_to_commit()
        self._check_timezones()

        # Check if from_commit and to_commit point to the same commit, in which case
        # we remove both filters and use the "single" filter instead. This prevents
        # errors with dates.
        if self.get("from_commit") and self.get("to_commit") and self.get("from_commit") == self.get("to_commit"):
            logger.warning("You should not point from_commit and to_commit to the same "
                           "commit, but use the 'single' filter instead.")
            single = self.get("to_commit")
            self.set_value("from_commit", None)
            self.set_value("to_commit", None)
            self.set_value("single", single)

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
                self.set_value('single', self.get("git").get_commit(self.get('single')).hash)
            except BadName:
                raise Exception("The commit {} defined in "
                                "the 'single' filtered does "
                                "not exist".format(self.get('single')))

    def _check_correct_filters_order(self):
        """
        Check that from_commit comes before to_commit
        """
        if self.get('from_commit') and self.get('to_commit'):
            chronological_order = self._is_commit_before(
                self.get('git').get_commit(self.get('from_commit')),
                self.get('git').get_commit(self.get('to_commit')))

            if not chronological_order:
                self._swap_commit_fiters()

    def _swap_commit_fiters(self):
        # reverse from and to commit
        from_commit = self.get('from_commit')
        to_commit = self.get('to_commit')
        self.set_value('from_commit', to_commit)
        self.set_value('to_commit', from_commit)

    @staticmethod
    def _is_commit_before(commit_before: Commit, commit_after: Commit):
        if commit_before.committer_date < commit_after.committer_date:
            return True
        if commit_before.committer_date == commit_after.committer_date and \
                commit_before.author_date < commit_after.author_date:
            return True
        return False

    def get_starting_commit(self):
        """
        Get the starting commit from the 'since', 'from_commit' or 'from_tag'
        filter.
        """
        from_tag = self.get('from_tag')
        from_commit = self.get('from_commit')
        if from_tag is not None:
            tagged_commit = self.get("git").get_commit_from_tag(from_tag)
            from_commit = tagged_commit.hash
        if from_commit is not None:
            try:
                commit = self.get("git").get_commit(from_commit)
                if len(commit.parents) == 0:
                    return [commit.hash]
                elif len(commit.parents) == 1:
                    return ['^' + commit.hash + '^']
                else:
                    return ['^' + x for x in commit.parents]
            except Exception:
                raise Exception("The commit {} defined in the 'from_tag' or 'from_commit' filter does "
                                "not exist".format(self.get('from_commit')))

    def get_ending_commit(self):
        """
        Get the ending commit from the 'to', 'to_commit' or 'to_tag' filter.
        """
        to_tag = self.get('to_tag')
        to_commit = self.get('to_commit')
        if to_tag is not None:
            tagged_commit = self.get("git").get_commit_from_tag(to_tag)
            to_commit = tagged_commit.hash
        if to_commit is not None:
            try:
                return self.get("git").get_commit(to_commit).hash
            except Exception:
                raise Exception("The commit {} defined in the 'to_tag' or 'to_commit' filter does "
                                "not exist".format(self.get('to_commit')))

    @staticmethod
    def only_one_filter(arr):
        """
        Return true if in 'arr' there is at most 1 filter to True.

        :param arr: iterable object
        :return:
        """
        return len([x for x in arr if x is not None]) <= 1

    def build_args(self):
        """
        This function builds the argument for git rev-list.

        :return:
        """
        single = self.get('single')
        since = self.get('since')
        until = self.get('to')
        from_commit = self.get_starting_commit()
        to_commit = self.get_ending_commit()
        include_refs = self.get('include_refs')
        remotes = self.get('include_remotes')
        branch = self.get('only_in_branch')
        authors = self.get('only_authors')
        order = self.get('order')
        rev = []
        kwargs = {}

        if single is not None:
            rev = [single, '-n', 1]
        elif from_commit is not None or to_commit is not None:
            if from_commit is not None and to_commit is not None:
                rev.extend(from_commit)
                rev.append(to_commit)
            elif from_commit is not None:
                rev.extend(from_commit)
                rev.append('HEAD')
            else:
                rev = to_commit
        elif branch is not None:
            rev = branch
        else:
            rev = 'HEAD'

        if self.get('only_no_merge'):
            kwargs['no-merges'] = True

        if not order:
            kwargs['reverse'] = True
        elif order == 'reverse':
            kwargs['reverse'] = False
        elif order == 'date-order':
            kwargs['date-order'] = True
        elif order == 'author-date-order':
            kwargs['author-date-order'] = True
        elif order == 'topo-order':
            kwargs['topo-order'] = True

        if include_refs is not None:
            kwargs['all'] = include_refs

        if remotes is not None:
            kwargs['remotes'] = remotes

        if authors is not None:
            kwargs['author'] = authors

        if since is not None:
            kwargs['since'] = since

        if until is not None:
            kwargs['until'] = until

        return rev, kwargs

    def is_commit_filtered(self, commit: Commit):
        # pylint: disable=too-many-branches,too-many-return-statements
        """
        Check if commit has to be filtered according to the filters provided
        by the user.

        :param Commit commit: Commit to check
        :return:
        """
        if self.get('only_modifications_with_file_types') is not None:
            if not self._has_modification_with_file_type(commit):
                logger.debug('Commit filtered for modification types')
                return True
        if self.get('only_commits') is not None and commit.hash not in self.get('only_commits'):
            logger.debug("Commit filtered because it is not one of the specified commits")
            return True
        if self.get('filepath_commits') is not None and commit.hash not in self.get('filepath_commits'):
            logger.debug("Commit filtered because it did not modify the specified file")
            return True
        if self.get('tagged_commits') is not None and commit.hash not in self.get('tagged_commits'):
            logger.debug("Commit filtered because it is not tagged")
            return True
        return False

    def _has_modification_with_file_type(self, commit):
        for mod in commit.modified_files:
            if mod.filename.endswith(tuple(self.get('only_modifications_with_file_types'))):
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
