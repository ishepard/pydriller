"""
Module that calculates the History Complexity Period Factor (HCPF) \
for the History Complexity Metric (HCM).

The History Complexity Metric can be calculated by calling the \
method count as many times as the evolution period to analyze and \
summing up the results.

E.g.

hcpf_1 = HistoryComplexity(..., from_commit=c1, to_commit=c2).count()
hcpf_2 = HistoryComplexity(..., from_commit=c3, to_commit=c4).count()

hcm = hcpf_1 + hcpf_2

See https://ieeexplore.ieee.org/document/5070510
"""

from math import log
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class HistoryComplexity(ProcessMetric):
    """
    This class is responsible to implement the History Complexity Metric. \
    The metric assigns to each modified file the effect of the change \
    complexity of an evolution period.
    """

    def count(self):
        """
        Calculate the History Complexity Period Factor for each modified file \
        in the provided period [from_commit, to_commit], returning the \
        probability of each file being modified during that period

        :return: dict
        {
            filepath: float
        }
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

                modifications = modified_file.added + modified_file.removed
                if modifications:
                    files[filepath] = files.get(filepath, 0) + modifications

        total_modifications = sum(files.values()) # Total lines modified in the period
        n_files = len(files) # Number of modified files in the period

        # From absolute number of changes to relative number of changes
        for filepath in files:
            files[filepath] /= total_modifications

        # Normalized entropy
        entropy = -sum(p*log(p+1/1e10, n_files) for p in files.values())

        for filepath in files:
            files[filepath] *= entropy
            files[filepath] = round(files[filepath] * 100, 2)

        return files
