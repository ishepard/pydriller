"""
This module provides an entry point to compute the following metrics:\
    * Commit Count: is the number of commits made to a file
    * Contributors Count: is the distinct number of developers who contributed \
      to a file.
    * Minor Contributor Count (MIN): measures the number of contributors who \
      authored less than 5% of the code of a file.
    * Normalized Lines Added: are the normalized (by the total number \
      of added lines) added lines in the file in a given time range.
    * History Complexity (SCTR): is the scattering of changes to a file.
    * Hunks Count (HUN): is the number of continuous block of changes in a diff.
    * Normalized Lines Deleted: are the normalized (by the total number \
      of deleted lines) deleted lines in the file in a given time range.

    * Owner's Contributed Lines: is the percentage of the lines authored by \
      the highest contributor of a file.
    * Owner's Experience: is the experience of the highest contributor of a file \
      using the percent of lines he authored in the project at a given point \
      in time.
    * All Committers' Experience (EXP): is the geometric mean of the experiences \
        of all the developers.
    * New Developers Count: is the number of new developers who modified \
      the file durint the prior release.

Note: All process metrics are cumulated and measured on a per-release basis.
See https://ieeexplore.ieee.org/document/6606589 for more info.
"""
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.contributors_count import ContributorsCount
from pydriller.metrics.process.history_complexity import HistoryComplexity
from pydriller.metrics.process.hunks_count import HunksCount
from pydriller.metrics.process.lines_count import NormalizedLinesCount

from pydriller.metrics.process.devs_experience import DevsExperience
from pydriller.metrics.process.new_devs_count import NewDevsCount

def commits_count(path_to_repo: str, from_commit: str = None, to_commit: str = None):
    return CommitsCount(path_to_repo,
                        from_commit=from_commit,
                        to_commit=to_commit).count()

def contributors_count(path_to_repo: str, from_commit: str = None, to_commit: str = None):
    return ContributorsCount(path_to_repo,
                             from_commit=from_commit,
                             to_commit=to_commit).count()

def history_complexity(path_to_repo: str, periods: list):
    """
    :periods: list of tuples (start, end) indicating the starting and ending commits for each
              period
    """
    results = []
    for from_commit, to_commit in periods:
        hcpf = HistoryComplexity(path_to_repo,
                               from_commit=from_commit,
                               to_commit=to_commit).count()

        results.append(hcpf)

    # Sum periods factors
    hcm = { 
      key: sum(d.get(key, 0) for d in results) for key in set().union(*results)
    }

    return hcm

def hunks_count(path_to_repo: str, from_commit: str = None, to_commit: str = None):
    return HunksCount(path_to_repo,
                      from_commit=from_commit,
                      to_commit=to_commit).count()

def norm_lines_count(path_to_repo: str, from_commit: str = None, to_commit: str = None):
    return NormalizedLinesCount(path_to_repo,
                                from_commit=from_commit,
                                to_commit=to_commit).count()

def devs_experience(path_to_repo: str, filepath: str, to_commit: str = None):
    return DevsExperience(path_to_repo, filepath,
                          to_commit=to_commit).count()


def news_devs_count(path_to_repo: str, filepath: str, to_commit: str = None):
    return NewDevsCount(path_to_repo, filepath, to_commit=to_commit).count()