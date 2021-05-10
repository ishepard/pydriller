"""
Module that calculates the experience of contributors of a file.
"""
from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class ContributorsExperience(ProcessMetric):
    """
    This class is responsible to implement the metric to measure the
    percentage of the lines authored by the highest contributor of a
    file in the provided evolution period [from_commit, to_commit].
    """

    def count(self):
        """
        Return the percentage of the lines authored by the highest contributor
        of a file for each modified file in the repository in the provided
        time range [from_commit, to_commit]

        :return: dict { filepath: float }
        of number of contributors for each modified file
        """
        renamed_files = {}
        files = {}

        for commit in self.repo_miner.traverse_commits():

            for modified_file in commit.modified_files:

                filepath = renamed_files.get(modified_file.new_path,
                                             modified_file.new_path)

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = filepath

                author = commit.author.email.strip()
                lines_authored = modified_file.added_lines + modified_file.deleted_lines

                files[filepath] = files.get(filepath, {})
                files[filepath][author] = files[filepath].get(author, 0) + \
                    lines_authored

        for path, contributions in list(files.items()):
            total = sum(contributions.values())
            if total == 0:
                del files[path]
            else:
                files[path] = round(100*max(contributions.values()) / total, 2)

        return files
