"""
Module that calculates process metrics.
See https://ieeexplore.ieee.org/document/6606589 for more info.
"""

from pathlib import Path
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining


class ProcessMetrics:
    """
    This class is responsible to implement the following process metrics:

    * Commit Count: measures the number of commits made to a file
    * Distinct Developers Count: measures the cumulative number of distinct \
    developers that contributed to a file
    """

    def commits_count(self, path_to_repo: str, filepath: str,
                      from_commit: str = None, to_commit: str = None):
        """
        Return the number of commits made to a file from the first commit to
        the one identified by commit_hash.

        :path_to_repo: path to a single repo
        :commit_hash: the SHA of the commit to stop counting. If None, the
            analysis starts from the latest commit
        :filepath: the path to the file to count for. E.g. 'doc/README.md'

        :return: int number of commits made to the file
        """

        filepath = str(Path(filepath))
        count = 0

        for commit in RepositoryMining(path_to_repo, from_commit=from_commit,
                                       to_commit=to_commit,
                                       reversed_order=True).traverse_commits():
            for modified_file in commit.modifications:
                if filepath in (modified_file.new_path,
                                modified_file.old_path):
                    count += 1

                    if modified_file.change_type == ModificationType.RENAME:
                        filepath = str(Path(modified_file.old_path))

                    break
        return count

    def distinct_dev_count(self, path_to_repo: str, filepath: str,
                           from_commit: str = None, to_commit: str = None):
        """
        Return the cumulative number of distinct developers contributed to
        the file up to the indicated commit.

        :path_to_repo: path to a single repo
        :commit_hash: the SHA of the commit to stop counting. If None,
            the SHA is the latest commit SHA
        :filepath: the path to the file to count for. E.g. 'doc/README.md'

        :return: int number of distinct developers contributing to the file
        """
        filepath = str(Path(filepath))
        developers = set()

        for commit in RepositoryMining(path_to_repo, from_commit=from_commit,
                                       to_commit=to_commit,
                                       reversed_order=True).traverse_commits():

            for modified_file in commit.modifications:
                if filepath in (modified_file.new_path,
                                modified_file.old_path):
                    developers.add(commit.author.email.strip())

                    if modified_file.change_type == ModificationType.RENAME:
                        filepath = str(Path(modified_file.old_path))

                    break

        return len(developers)
