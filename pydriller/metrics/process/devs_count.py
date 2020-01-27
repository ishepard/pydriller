"""
Module that calculates the number of developers that contributed to each modified file \
    in the repo in a given time range.
"""
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class DevsCount(ProcessMetric):
    """
    This class counts the number of developers who changed the file \
        in the given time range [from_commit, to_commit].
    """

    def count(self):
        """
        Return a dictionary with the number of distinct developers who \
            contributed to each modified file.
            The key is the modified filepath;
            The value is the number of developers that changed it.

        :return: dict {str: int}
        """
        renamed_files = {}
        files = {}

        for commit in RepositoryMining(path_to_repo=self.path_to_repo,
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            for modified_file in commit.modifications:

                filepath = renamed_files.get(modified_file.new_path,
                                             modified_file.new_path)

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = filepath

                developer = commit.author.email.strip()

                if filepath not in files:
                    files[filepath] = set([developer])

                files[filepath].add(developer)

        for path, devs in files.items():
            files[path] = len(devs)

        return files
