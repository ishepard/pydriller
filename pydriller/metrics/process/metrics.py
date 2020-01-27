"""
Module to calculate the following process metrics for a file \
at a given commit:

    * Commit Count: is the number of commits made to a file
    * Active Developers Count: is the number of developers who contributed \
      to the file
    * Distinct Developers Count: is the cumulative number of distinct \
      developers who contributed to the file
    * New Developers Count: is the number of new developers who modified \
      the file durint the prior release.
    * Normalized Lines Added: are the normalized (by the total number \
      of added lines) added lines in the file
    * Normalized Lines Deleted: are the normalized (by the total number \
      of deleted lines) deleted lines in the file
    * Owner's Contributed Lines: is the percentage of the lines authored by \
      the highest contributor of a file.
    * Owner's Experience: is the experience of the highest contributor of a file \
      using the percent of lines he authored in the project at a given point \
      in time.
    * All Committers' Experience (EXP): is the geometric mean of the experiences \
        of all the developers.
    * Minor Contributor Count (MIN): measures the number of contributors who \
      authored less than 5% of the code of a file.
    * Hunks Count (HUN): is the number of continuous block of changes in a diff.
    * History Complexity (SCTR): is the scattering of changes to a file.

Note: All process metrics are cumulated and measured on a per-release basis.
See https://ieeexplore.ieee.org/document/6606589 for more info.
"""

from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.devs_count import DevsCount
from pydriller.metrics.process.devs_experience import DevsExperience
from pydriller.metrics.process.history_complexity import HistoryComplexity
from pydriller.metrics.process.hunks_count import HunksCount
from pydriller.metrics.process.lines_count import NormalizedLinesCount
from pydriller.metrics.process.minor_contributor_count import MinorContributorCount
from pydriller.metrics.process.new_devs_count import NewDevsCount

def commits_count(path_to_repo: str, from_commit: str = None, to_commit: str = None):
    return CommitsCount(path_to_repo, from_commit=from_commit, to_commit=to_commit).count()

def devs_count(path_to_repo: str, filepath: str, to_commit: str = None):
    return DevsCount(path_to_repo, filepath, to_commit=to_commit).count()

def devs_experience(path_to_repo: str, filepath: str, to_commit: str = None):
    return DevsExperience(path_to_repo, filepath,
                          to_commit=to_commit).count()

def history_complexity(path_to_repo: str, filepath: str, to_commit: str = None):
    return HistoryComplexity(path_to_repo, filepath,
                      to_commit=to_commit).count()

def hunks_count(path_to_repo: str, filepath: str, to_commit: str = None):
    return HunksCount(path_to_repo, filepath,
                      to_commit=to_commit).count()

def minor_contributors_count(path_to_repo: str, filepath: str, to_commit: str = None):
    return MinorContributorCount(path_to_repo, filepath,
                                 to_commit=to_commit).count()

def news_devs_count(path_to_repo: str, filepath: str, to_commit: str = None):
    return NewDevsCount(path_to_repo, filepath, to_commit=to_commit).count()

def norm_lines_count(path_to_repo: str, filepath: str, to_commit: str = None):
    return NormalizedLinesCount(path_to_repo, filepath,
                                to_commit=to_commit).count()
