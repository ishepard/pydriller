"""
Module that calculates the experience of contributors of a file.
"""
import math
from pathlib import Path
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class DevsExperience(ProcessMetric):
    """
    This class is responsible to implement the following metrics:

    * Owner's Contributed Lines (OWN): is the percentage of the lines \
        authored by the highest contributor of a file.
    * Owner's Experience (OEXP): is the experience of the highest contributor \
        of a file using the percent of lines he authored in the project at a \
        given point in time.
    * All Committers' Experience (EXP): is the geometric mean of the \
        experiences of all the developers.
    """

    def count(self):
        """
        Return a tuple (OWN, OEXP, EXP). See class doc for more information.

        :return: a tuple of float between 0 and 1 - percentage of lines authored
        """

        contributors = {}
        filepath = self.filepath
        is_release_contribution = True

        for commit in RepositoryMining(path_to_repo=self.path_to_repo,
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            author = commit.author.email.strip()
            if author not in contributors:
                contributors[author] = {
                    'file_contribution': 0,
                    'release_contribution': 0,
                    'project_contribution': 0
                }

            for modified_file in commit.modifications:

                lines_authored = modified_file.added + modified_file.removed
                contributors[author]['project_contribution'] += lines_authored

                if is_release_contribution:
                    contributors[author]['release_contribution'] += lines_authored

                if filepath in (modified_file.new_path,
                                modified_file.old_path):

                    if is_release_contribution:
                        contributors[author]['file_contribution'] += lines_authored

                    if modified_file.change_type == ModificationType.RENAME:
                        filepath = str(Path(modified_file.old_path))

            if commit.hash in self.releases:
                # Stop counting active experience (release scope)
                is_release_contribution = False

        highest_contributor = None
        highest_release_contribution = 0
        total_project_contribution = 0
        total_release_contribution = 0
        
        # The geometric means of all the developers
        geo_experience = 1

        for c in contributors.items():
            geo_experience *= c[1]['project_contribution']
            total_project_contribution += c[1]['project_contribution']
            total_release_contribution += c[1]['release_contribution']

            file_contribution = c[1]['file_contribution']
            if file_contribution > highest_release_contribution:
                highest_contributor = c[0] # author name
                highest_release_contribution = file_contribution

        if not highest_contributor:
            return (0, 0, 0)

        own = round(highest_release_contribution/total_release_contribution, 4)
        oexp = round(contributors[highest_contributor]['project_contribution']/total_project_contribution, 4)
        geo_experience = round(math.pow(geo_experience, 1/len(contributors)), 2)

        return (own, oexp, geo_experience)
      