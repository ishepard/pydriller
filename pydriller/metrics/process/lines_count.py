"""
Module that calculates the number of normalized added and deleted lines of a file.
"""
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class NormalizedLinesCount(ProcessMetric):
    """
    This class is responsible to implement the following metrics: \
    * Normalized Added Lines: is the number of added lines in a file \
        of a given commit over the total number of added lines in the \
        provided time range, e.g. a [from_commit, to_commit] representing \
        a release.
    * Normalized Deleted Lines: is the number of deleted lines in a file \
        of a given commit over the total number of deleted lines in the \
        provided time range, e.g. a [from_commit, to_commit] representing \
        a release.
    """

    def count(self):
        """
        Calculate the number of normalized (by the total number of added and \
        deleted lines) added and deleted lines per each modified file in \
        'to_commit', returning a dictionary:
        {filepath: {
            added: float,
            removed: float}
        }

        :return: dict of normalized added and deleted lines per modified file
        """
        renamed_files = {}
        files = {}

        for commit in RepositoryMining(self.path_to_repo,
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            for modified_file in commit.modifications:

                filepath = renamed_files.get(modified_file.new_path,
                                             modified_file.new_path)

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = filepath

                if commit.hash == self.to_commit:
                    files[filepath] = files.get(filepath,
                                                {'added': 0,            # Added in to_commit
                                                 'removed': 0,          # Removed in to_commit
                                                 'total_added': 0,      # Added in time range [from_commit, to_commit]
                                                 'total_removed': 0})   # Removed in time range [from_commit, to_commit]
                    files[filepath]['added'] += modified_file.added
                    files[filepath]['removed'] += modified_file.removed

                if filepath in files:
                    files[filepath]['total_added'] += modified_file.added
                    files[filepath]['total_removed'] += modified_file.removed

        for path in list(files.keys()):
            if files[path]['total_added']:
                files[path]['added'] = round(100 * files[path]['added'] / files[path]['total_added'], 2)

            if files[path]['total_removed']:
                files[path]['removed'] = round(100 * files[path]['removed'] / files[path]['total_removed'], 2)

            del files[path]['total_added']   # Remove key 'total_added': not useful anymore
            del files[path]['total_removed'] # Remove key 'total_removed': not useful anymore

        return files
