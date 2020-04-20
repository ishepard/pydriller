"""
Module that calculates the number of normalized added and deleted lines of a
file.
"""
import statistics
from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class LinesCount(ProcessMetric):
    """
    This class is responsible to implement the following metrics:

    * Changed Lines: the number of added and deleted lines in the evolution
        period [from_commit, to_commit]

    * Added Lines: the sum over all commits of the lines of code added to a
        file in the evolution period [from_commit, to_commit]

    * Max Added Lines: the maximum number of lines of code added to a file
        per commit in the evolution period [from_commit, to_commit]

    * Average Added Lines: the average lines of code added to a file per commit
        in the evolution period [from_commit, to_commit]

    * Removed Lines: the sum over all commits of the lines of code removed to a
        file in the evolution period [from_commit, to_commit]

    * Max Removed Lines: the maximum number of lines of code removed to a file
        per commit in the evolution period [from_commit, to_commit]

    * Average Removed Lines: the average lines of code removed to a file per
        commit in the evolution period [from_commit, to_commit]

    """

    def __init__(self, path_to_repo: str,
                 since=None,
                 to=None,
                 from_commit: str = None,
                 to_commit: str = None):

        super().__init__(path_to_repo, since=since, to=to, from_commit=from_commit, to_commit=to_commit)
        self._initialize()

    def _initialize(self):

        self.lines_added = dict()
        self.lines_removed = dict()

        renamed_files = {}
        for commit in self.repo_miner.traverse_commits():

            for modified_file in commit.modifications:

                filepath = renamed_files.get(modified_file.new_path,
                                             modified_file.new_path)

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = filepath

                self.lines_added.setdefault(filepath, []).append(modified_file.added)
                self.lines_removed.setdefault(filepath, []).append(modified_file.removed)

    def count(self):
        """
        Sum over all commits of the lines of code added and removed to a file .

        :return: int lines added + lines removed
        """
        count = dict()

        for path, lines in self.lines_added.items():
            count[path] = count.get(path, 0) + sum(lines)

        for path, lines in self.lines_removed.items():
            count[path] = count.get(path, 0) + sum(lines)

        return count

    def count_added(self):
        """
        Sum over all commits of the lines of code added to a file .

        :return: int lines added
        """
        count = dict()
        for path, lines in self.lines_added.items():
            count[path] = sum(lines)

        return count

    def max_added(self):
        """
        Maximum number of lines of code added to a file for all commits

        :return: int max number of lines added
        """
        maximum = dict()
        for path, lines in self.lines_added.items():
            maximum[path] = max(lines)

        return maximum

    def avg_added(self):
        """
        Average lines of code added to a file per commit

        :return: int avg number of lines rounded off to the nearest integer
        """
        avg = dict()
        for path, lines in self.lines_added.items():
            avg[path] = round(statistics.mean(lines))

        return avg

    def count_removed(self):
        """
        Sum over all commits of the lines of code removed to a file .

        :return: int lines removed
        """
        count = dict()
        for path, lines in self.lines_removed.items():
            count[path] = sum(lines)

        return count

    def max_removed(self):
        """
        Maximum number of lines of code removed in a file for all commits

        :return: int max number of lines removed
        """
        maximum = dict()
        for path, lines in self.lines_removed.items():
            maximum[path] = max(lines)

        return maximum

    def avg_removed(self):
        """
        Average lines of code removed in a file per commit

        :return: int rounded off to the nearest integer
        """
        avg = dict()
        for path, lines in self.lines_removed.items():
            avg[path] = round(statistics.mean(lines))

        return avg
