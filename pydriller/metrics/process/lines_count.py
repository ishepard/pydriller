"""
Module that calculates the number of normalized added and deleted lines of a
file.
"""
from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class LinesCount(ProcessMetric):
    """
    This class is responsible to implement the following metrics:
    * Added Lines: the number of added lines in the evolution period
        [from_commit, to_commit]
    * Deleted Lines: the number of deleted lines in the evolution period
        [from_commit, to_commit]
    """

    def count(self):
        """
        Calculate the number of normalized (by the total number of added and
        deleted lines) added and deleted lines per each modified file in
        'to_commit', returning a dictionary:
        {
          filepath: {
            added: int,
            removed: int
          }
        }

        :return: dict of total added and deleted lines per modified file
        """
        renamed_files = {}
        files = {}

        for commit in self.repo_miner.traverse_commits():

            for modified_file in commit.modifications:

                filepath = renamed_files.get(modified_file.new_path,
                                             modified_file.new_path)

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = filepath

                if filepath not in files:
                    files[filepath] = {'added': 0, 'removed': 0}
                files[filepath]['added'] += modified_file.added
                files[filepath]['removed'] += modified_file.removed

        return files
