"""
Module that calculates the number of commits made to a file.
"""

from pathlib import Path
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric


class CommitCount(ProcessMetric):
    """
    This class is responsible to implement the Commit Count metric to \
    measure the number of commits made to a file
    """


    def count(self):
        count = 0
        filepath = self.filepath

        for commit in RepositoryMining(path_to_repo=self.path_to_repo, 
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            for modified_file in commit.modifications:

                if filepath in (modified_file.new_path,
                                modified_file.old_path):
                    count += 1
                    if modified_file.change_type == ModificationType.RENAME:
                        filepath = str(Path(modified_file.old_path))

                    break

            if self.release_scope and commit.hash in self.releases:
                break

        return count
