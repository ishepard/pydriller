"""
Module that calculates the History Complexity Metric.

See https://ieeexplore.ieee.org/document/5070510
"""
from enum import Enum
from math import log
from pathlib import Path
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class HistoryPeriod(Enum):
    RELEASE  = 0,
    WEEK = 1,
    MONTH = 2,
    YEAR = 3,
    ALL = 4

class HistoryComplexity(ProcessMetric):
    """
    This class is responsible to implement the History Complexity Metric for \
    a given file. The metric assigns to that file the effect of the change \
    complexity of a period.
    """

    def count(self, period: HistoryPeriod = HistoryPeriod.RELEASE):
        """
        Return the history complexity (HCM) of a file as a tuple \
            (hcm_c1, hcm_cp, hcm_cu) where:
        - hcm_c1 is the value of the HCM calculated assigning the full \
            complexity value to every modified file in the period;
        - hcm_cp is the value of the HCM calculated assigning a percentage \
            of complexity associated to the period. The percentage is the \
            probability of file being modified during that period;
        - hcm_cu is the value of the HCM calculated distributing evenly \
            the complexity associated to the period between all modified \
            files in that period.

        The considered period is from the start of the release the file \
            belongs to, up to the file itself.

        :period: the period of time to perform the analysis. \
            Can be RELEASE, WEEK, MONTH, ALL

        :return: a tuple of float
        """
        filepath = self.filepath

        # the change probability distribution for the considered period
        renaming = {}
        change_prob_dist = {}
        to_date = None
        periods = []
        for commit in RepositoryMining(path_to_repo=self.path_to_repo,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            commit_date = commit.committer_date

            if not to_date:
                to_date = commit_date

            for modified_file in commit.modifications:

                # Handling recursive renaming
                if modified_file.new_path in renaming:
                    new_path = renaming.get(modified_file.new_path, None)
                else:
                    new_path = modified_file.new_path

                if modified_file.change_type == ModificationType.RENAME:
                    renaming[modified_file.old_path] = new_path

                # Updating changes
                changes = modified_file.added + modified_file.removed

                if new_path in change_prob_dist:
                    change_prob_dist[new_path] += changes
                else:
                    change_prob_dist[new_path] = changes

            if (period == HistoryPeriod.RELEASE and commit.hash in self.releases) or \
               (period == HistoryPeriod.WEEK and (to_date - commit_date).days >= 7) or \
               (period == HistoryPeriod.MONTH and (to_date - commit_date).days >= 28):  # Considering 4 weeks

                periods.append(change_prob_dist)
                change_prob_dist = {}
                to_date = commit_date
        
        if period == HistoryPeriod.ALL:
            periods.append(change_prob_dist)

        hcm_c1 = hcm_cp = hcm_cu = 0

        for distribution in periods:

            # total_changes
            n = sum(distribution.values())

            # Store the relative frequencies of chages per file
            for p in distribution:
                distribution[p] /= n

            norm_entropy = sum(-(p*log(p+1/1000000, n)) for p in distribution.values())

            # Calculate the History Complexity Period Factor of the file, where period=release
            hcm_c1 += norm_entropy
            hcm_cp += distribution.get(filepath, 0) * norm_entropy
            hcm_cu += (1/n) * norm_entropy

        return((round(hcm_c1, 4), round(hcm_cp, 4), round(hcm_cu, 4)))
