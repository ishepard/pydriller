"""
Module that calculates the number of developers that contributed to a file
"""
from pathlib import Path
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class DevsCount(ProcessMetric):
    """
    This class is responsible to implement the following metrics: \
    * Active Developers Count: is the number of developers who changed \
        the file in the commit release.
    * Distinct Developers Count: is the cumulative number of distinct \
        developers who contributed to the file up to the commit release.
    """

    def count(self):
        """
        Return the active or cumulative number of distinct developers who
        contributed to the file up to the indicated commit.

        :return: a tuple (int, int) indicating the number of distinct
            cumulative and active developers contributing to the file.
            E.g. (5, 2) means that 5 distinct developers modified the
            file during is history, 2 of which in the release the commit
            belongs to.
        """
        active_devs = set()
        cumulative_devs = set()
        filepath = self.filepath

        count_active_devs = True

        for commit in RepositoryMining(path_to_repo=self.path_to_repo,
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            for modified_file in commit.modifications:
                if filepath in (modified_file.new_path,
                                modified_file.old_path):

                    cumulative_devs.add(commit.author.email.strip())

                    if count_active_devs:
                        active_devs.add(commit.author.email.strip())

                    if modified_file.change_type == ModificationType.RENAME:
                        filepath = str(Path(modified_file.old_path))

                    break

            if commit.hash in self.releases:
                count_active_devs = False

        return (len(cumulative_devs), len(active_devs))
        