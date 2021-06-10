"""
Module that calculates the number of hunks made to a commit file.
"""
import statistics

from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class CodeChurn(ProcessMetric):
    """
    This class is responsible to implement the Code Churn metric for a file.
    Depending on the parametrization of this class, a code churn is the sum of either
    (added lines - removed lines) or
    (added lines + removed lines)
    across the analyzed commits. It allows to count for the:
    * total number of code churns - count();
    * maximum code churn for all commits - max();
    * average code churn per commit.
    """

    def __init__(self, path_to_repo: str,
                 since=None,
                 to=None,
                 from_commit: str = None,
                 to_commit: str = None,
                 ignore_added_files=False,
                 add_deleted_lines_to_churn=False):
        """
        :ignore_added_files: if True, do not count churns for files when created
        :add_deleted_lines_to_churn: if True, also add deleted lines to churn calculation
        """

        super().__init__(path_to_repo, since=since, to=to, from_commit=from_commit, to_commit=to_commit)
        self.ignore_added_files = ignore_added_files
        self.add_deleted_lines_to_churn = add_deleted_lines_to_churn
        self._initialize()

    def _initialize(self):

        renamed_files = {}
        self.files = {}

        for commit in self.repo_miner.traverse_commits():

            for modified_file in commit.modified_files:

                filepath = renamed_files.get(modified_file.new_path, modified_file.new_path)

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = filepath

                if self.ignore_added_files and modified_file.change_type == ModificationType.ADD:
                    continue

                if self.add_deleted_lines_to_churn:
                    churn = modified_file.added_lines + modified_file.deleted_lines
                else:
                    churn = modified_file.added_lines - modified_file.deleted_lines

                self.files.setdefault(filepath, []).append(churn)

    def count(self):
        """
        Return the total number of code churns for each modified file.

        :return: int number of churns
        """
        count = {}
        for path, churns in self.files.items():
            count[path] = sum(churns)

        return count

    def max(self):
        """
        Return the maximum code churn for each modified file.

        :return: int max number of churns
        """
        max_count = {}
        for path, churns in self.files.items():
            max_count[path] = max(churns)

        return max_count

    def avg(self):
        """
        Return the average number of code churns for each modified file.

        :return: int avg number of churns rounded off to the nearest integer
        """
        avg_count = {}
        for path, churns in self.files.items():
            avg_count[path] = round(statistics.mean(churns))

        return avg_count
