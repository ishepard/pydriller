"""
Module that calculates the experience of the highest contributor of a file.
"""
from pathlib import Path
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class OwnerExperience(ProcessMetric):
    """
    This class is responsible to implement the following metrics:
    * Owner's Contributed Lines (OWN): is the percentage of the lines authored by \
        the highest contributor of a file.
    * Owner's Experience (OEXP): is the experience of the highest contributor of a file \
        using the percent of lines he authored in the project at a given point \
        in time.
    """

    def count(self):
        """
        Return a tupe (OWN, OEXP) the percentage of the lines authored by the highest contributor
        of a file in the project.

        :return: a tuple of float between 0 and 1 - percentage of lines authored
        """
        contributions = {}
        filepath = self.filepath
        is_release_contribution = True

        total_project_contributions = 0

        for commit in RepositoryMining(path_to_repo=self.path_to_repo,
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            for modified_file in commit.modifications:

                lines_authored = modified_file.added + modified_file.removed
                total_project_contributions += lines_authored

                if filepath in (modified_file.new_path,
                                modified_file.old_path):

                    author = commit.author.email.strip()

                    if author not in contributions:
                        # [release contribution, project contributions]
                        contributions[author] = [0, 0]

                    if is_release_contribution:
                        contributions[author][0] += lines_authored

                    contributions[author][1] += lines_authored

                    if modified_file.change_type == ModificationType.RENAME:
                        filepath = str(Path(modified_file.old_path))

            if commit.hash in self.releases:
                # Stop counting active experience (release scope)
                is_release_contribution = False

        # Return the highest value from the dictionary of contributions
        if contributions.values():
            highest_contribution = 0
            highest_experience = 0
            total_release_experience = 0

            for c in contributions.items():
                author = c[0]
                active_experience = c[1][0]
                project_experience = c[1][1]
                total_release_experience += active_experience

                if active_experience > highest_contribution:
                    highest_contribution = active_experience
                    highest_experience = project_experience

            perc_release = round(highest_contribution/total_release_experience, 4)
            perc_project = round(highest_experience/total_project_contributions, 4)
            return (perc_release, perc_project)

        return (.0, .0)
      