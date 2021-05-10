"""
Module that calculates the number of files committed together.
"""
import statistics

from pydriller.metrics.process.process_metric import ProcessMetric


class ChangeSet(ProcessMetric):
    """
    This class is responsible to implement the Change Set metric that
    measures the

    * maximum number of files committed together - max();
    * average number of files committed together - avg().
    """

    def __init__(self, path_to_repo: str,
                 since=None,
                 to=None,
                 from_commit: str = None,
                 to_commit: str = None):

        super().__init__(path_to_repo, since=since, to=to, from_commit=from_commit, to_commit=to_commit)
        self._initialize()

    def _initialize(self):

        self.committed_together = []

        for commit in self.repo_miner.traverse_commits():
            self.committed_together.append(len(commit.modified_files))

    def max(self):
        """
        Return the maximum number of files committed together.

        :return: int max number of files committed together
        """
        return max(self.committed_together, default=0)

    def avg(self):
        """
        Return the average number of files committed together.

        :return: int avg number of files rounded off to the nearest integer
        """
        if not self.committed_together:
            return 0

        return round(statistics.mean(self.committed_together))
