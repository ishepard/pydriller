"""
Module that calculates the number of hunks made to a commit file.
"""
from statistics import median

from pydriller.domain.commit import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric
from pydriller.repository_mining import RepositoryMining

class HunksCount(ProcessMetric):
    """
    This class is responsible to implement the Number of Hunks metric for a file. \
    As a hunk is a continuous block of changes in a diff, this number assesses \
    how fragmented the commit file is (i.e. lots of changes all over the file \
    versus one big change).
    
    If multiple commits are passed, it returns the median number of hunks in that range.
    """

    def count(self):
        """
        Return the number of hunks for each modified file.

        :return: int number of hunks
        """
        renamed_files = {}
        files = {}

        for commit in RepositoryMining(path_to_repo=self.path_to_repo,
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit).traverse_commits():

            for modified_file in commit.modifications:

                filepath = renamed_files.get(modified_file.new_path,
                                             modified_file.new_path)

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = filepath

                diff = modified_file.diff
                is_hunk = False
                hunks = 0

                for line in diff.splitlines():
                    if line.startswith('+') or line.startswith('-'):
                        if not is_hunk:
                            is_hunk = True
                            hunks += 1
                    else:
                        is_hunk = False

                if filepath in files:
                    files[filepath].append(hunks)
                else:
                    files[filepath] = [hunks]

        for path, hunks in files.items():
            files[path] = median(hunks)

        return files
