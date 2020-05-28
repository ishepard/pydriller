"""
Module that calculates the number of hunks made to a commit file.
"""
import statistics

from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class CodeChurn(ProcessMetric):
    """
    This class is responsible to implement the Code Churn metric for a
    file.
    A code churn is the sum of (added lines - removed lines) across the
    analyzed commits.
    It allows to count for the:
    * total number of code churns - count();
    * maximum code churn for all commits - max();
    * average code churn per commit.
    """

    def __init__(self, path_to_repo: str,
                 since=None,
                 to=None,
                 from_commit: str = None,
                 to_commit: str = None):

        super().__init__(path_to_repo, since=since, to=to, from_commit=from_commit, to_commit=to_commit)
        self._initialize()

    def _initialize(self):

        renamed_files = {}
        self.files = {}

        for commit in self.repo_miner.traverse_commits():

            for modified_file in commit.modifications:

                filepath = renamed_files.get(modified_file.new_path, modified_file.new_path)

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = filepath

                churn = modified_file.added - modified_file.removed
                self.files.setdefault(filepath, []).append(churn)

    def count(self):
        """
        Return the total number of code churns for each modified file.

        :return: int number of churns
        """
        count = dict()
        for path, churns in self.files.items():
            count[path] = sum(churns)

        return count

    def max(self):
        """
        Return the maximum code churn for each modified file.

        :return: int max number of churns
        """
        max_count = dict()
        for path, churns in self.files.items():
            max_count[path] = max(churns)

        return max_count

    def avg(self):
        """
        Return the average number of code churns for each modified file.

        :return: int avg number of churns rounded off to the nearest integer
        """
        avg_count = dict()
        for path, churns in self.files.items():
            avg_count[path] = round(statistics.mean(churns))

        return avg_count
