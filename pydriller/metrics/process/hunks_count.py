"""
Module that calculates the number of hunks made to a commit file.
"""

from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric


class HunksCount(ProcessMetric):
    """
    This class is responsible to implement the Number of Hunks metric for a file. \
        As a hunk is a continuous block of changes in a diff, this number assesses \
        how fragmented the commit file is (i.e. lots of changes all over the file \
        versus one big change).
    """

    def count(self):
        """
        Return the number of hunks for the file.

        :return: int number of hunks
        """
        count = 0
        filepath = self.filepath

        for commit in RepositoryMining(path_to_repo=self.path_to_repo,
                                       single=self.to_commit).traverse_commits():

            for modified_file in commit.modifications:

                if filepath in (modified_file.new_path,
                                modified_file.old_path):
                    
                    diff = modified_file.diff
                    hunk = False

                    for line in diff.splitlines():
                        if line.startswith('+') or line.startswith('-'):
                            if not hunk:
                                hunk = True
                                count += 1
                        else:
                            hunk = False

        return count
