"""
This module contains the abstract class to implement process metrics.
"""

from pydriller import RepositoryMining

class ProcessMetric:
    """
    Abstract class to implement process metrics
    """

    def __init__(self, path_to_repo: str,
                 from_commit: str,
                 to_commit: str):
        """
        :path_to_repo: path to a single repo
        :to_commit: the SHA of the commit to stop counting. If None, the
            analysis starts from the latest commit
        :from_commit: the SHA of the commit to start counting. If None, the
            analysis ends to the first commit
        """
        if not from_commit or not to_commit:
            raise TypeError

        self.repo_miner = RepositoryMining(path_to_repo, single=from_commit)

        if from_commit != to_commit:
            self.repo_miner = RepositoryMining(path_to_repo=path_to_repo,
                                               from_commit=from_commit,
                                               to_commit=to_commit,
                                               reversed_order=True)

    def count(self):
        """
        Implement the main functionality of the metric
        """
        return 0
