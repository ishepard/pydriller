"""
Module that calculates the number of contributors who authored less than 5% \
    of the code in a file

See https://dl.acm.org/doi/10.1145/2025113.2025119
"""
from pathlib import Path
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class MinorContributorCount(ProcessMetric):
    """
    This class is responsible to implement the metrics "Minor Contributor \
        Count" that measures the number of contributors who authored less \
        than 5% of code of a file.
    """

    def count(self):
        """
        Return the number of contributors who authored less than 5% of code \
            of a file

        :return: int number of contributors
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

        # Return the # of contributors with < 5% on the file
        if contributions.values():
            total = sum(contributions.values())
            return sum(1 for v in contributions.values() if v/total < .05)

        return 0
