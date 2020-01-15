"""
Module that calculates the number of developers that contributed to a file
"""
from pathlib import Path
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class OwnersContributedLines(ProcessMetric):
    """
    This class is responsible to implement the metrics "Owner's Contributed \
        Lines" that measures the percentage of the lines authored by the \
        highest contributor of a file.
    """

    def count(self):
        """
        Return the percentage of the lines authored by the highest contributor
        of a file.

        :return: float between 0 and 1 - percentage of lines
        """
        contributions = {}
        filepath = self.filepath

        for commit in RepositoryMining(path_to_repo=self.path_to_repo,
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            for modified_file in commit.modifications:
                if filepath in (modified_file.new_path,
                                modified_file.old_path):

                    lines_authored = modified_file.added + modified_file.removed

                    author = commit.author.email.strip()

                    if author not in contributions:
                        contributions[author] = lines_authored
                    else:
                        contributions[author] += lines_authored

                    if modified_file.change_type == ModificationType.RENAME:
                        filepath = str(Path(modified_file.old_path))

                    break

            if commit.hash in self.releases:
                break

        # Return the highest value from the dictionary of contributions
        highest = total = 0

        if contributions.values():
            highest = max(contributions.values())
            total = sum(contributions.values())

        if total == 0:
            return 0.0

        return float(highest/total)
        