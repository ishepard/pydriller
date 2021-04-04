"""
This module contains the abstract class to implement process metrics.
"""

from datetime import datetime
from pydriller import Repository


class ProcessMetric:
    """
    Abstract class to implement process metrics
    """

    def __init__(self, path_to_repo: str,
                 since: datetime = None,
                 to: datetime = None,
                 from_commit: str = None,
                 to_commit: str = None):
        """
        :path_to_repo: path to a single repo

        :param datetime since: starting date

        :param datetime to: ending date

        :param str from_commit: starting commit (only if `since` is None)

        :param str to_commit: ending commit (only if `to` is None)
        """

        if not since and not from_commit:
            raise TypeError('You must pass one between since and from_commit')

        if not to and not to_commit:
            raise TypeError('You must pass one between to and to_commit')

        if from_commit and to_commit and from_commit == to_commit:  # Use 'single' param to avoid Warning
            self.repo_miner = Repository(path_to_repo, single=from_commit)

        else:
            self.repo_miner = Repository(path_to_repo=path_to_repo,
                                         since=since,
                                         to=to,
                                         from_commit=from_commit,
                                         to_commit=to_commit,
                                         order='reverse')

    def count(self):
        """
        Implement the main functionality of the metric
        """
        return 0
