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
                 from_commit: str,
                 to_commit: str):
        super().__init__(path_to_repo, from_commit, to_commit)
        self._initialize()

    def _initialize(self):

        self.committed_together = []

        for commit in self.repo_miner.traverse_commits():
            self.committed_together.append(len(commit.modifications))

    def max(self):
        """
        Return the maximum number of files committed together.

        :return: int max number of files committed together
        """
        return max(self.committed_together)

    def avg(self):
        """
        Return the average number of files committed together.

        :return: int avg number of files rounded off to the nearest integer
        """

        return round(statistics.mean(self.committed_together))
