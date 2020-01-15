"""
Module that calculates the number of normalized added and deleted lines of a file.
"""
from pathlib import Path
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class NormalizedLinesCount(ProcessMetric):
    """
    This class is responsible to implement the following metrics: \
    * Normalized Added Lines: is the number of added lines in a file \
        of a given commit over the total number of added lines in the   
        release the commit belongs to.
    * Normalized Deleted Lines: is the number of deleted lines in a file \
        of a given commit over the total number of deleted lines in the
        release the commit belongs to.
    """

    def count(self):
        """
        Return the number of normalized (by the total number of added lines)
        added and deleted lines in the file.

        :return: a tuple of float normalized added and deleted lines,
            respectively.
            E.g. (0.6, 0.2) indicates that 60% of the total added lines of a
            file in the release have been added at the specified commit, while
            20% of the total deleted lines of that file in the release have
            been deleted at the specified commit.
        """
        filepath = self.filepath
        total_added = 0
        total_deleted = 0
        added = 0
        deleted = 0

        for commit in RepositoryMining(self.path_to_repo,
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            for modified_file in commit.modifications:
                if filepath in (modified_file.new_path,
                                modified_file.old_path):

                    if commit.hash == self.to_commit:
                        added = modified_file.added
                        deleted = modified_file.removed

                    total_added += modified_file.added
                    total_deleted += modified_file.removed

                    if modified_file.change_type == ModificationType.RENAME:
                        filepath = str(Path(modified_file.old_path))

                    break

            if commit.hash in self.releases:
                break

        if total_added == 0:
            norm_added = 0
        else:
            norm_added = float(added/total_added)

        if total_deleted == 0:
            norm_deleted = 0
        else:
            norm_deleted = float(deleted/total_deleted)

        return (norm_added, norm_deleted)
        