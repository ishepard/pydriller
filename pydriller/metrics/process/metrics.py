"""
This module provides an entry point to compute the following metrics:\
    * Commit Count: is the number of commits made to a file \
        -> commits_count(...)

    * Contributors Count: is the distinct number of developers who contributed \
      to a file.
        -> contributors_count(...)[filepath]['contributors_count']

    * Minor Contributor Count: measures the number of contributors who \
      authored less than 5% of the code of a file.
        -> contributors_count(...)[filepath]['minor_contributors_count']

    * Highest Contributor's Experience: is the percentage of the lines authored by \
      the highest contributor of a file.
        -> highest_contributors_experience(...)

    * History Complexity: is the scattering of changes to a file.
        -> history_complexity(...)

    * Hunks Count: is the number of continuous block of changes in a diff.
        -> hunks_count(...)
        
    * Added Lines: the number of added lines in commit 'to_commit'
        -> lines_count(...)[filepath]['added']

    * Deleted Lines: the number of deleted lines in commit 'to_commit'
        -> lines_count(...)[filepath]['removed']

    * Normalized Lines Added: are the normalized (by the total number \
      of added lines) added lines in the file in a given time range.
        -> lines_count(...)[filepath]['norm_added']

    * Normalized Lines Deleted: are the normalized (by the total number \
      of deleted lines) deleted lines in the file in a given time range.
        -> lines_count(...)[filepath]['norm_removed']

    * Total Added Lines: the number of added lines in the evolution period \
        [from_commit, to_commit]
        -> lines_count(...)[filepath]['total_added']

    * Total Deleted Lines: the number of deleted lines in the evolution period \
        [from_commit, to_commit]
        -> lines_count(...)[filepath]['total_removed']

See https://ieeexplore.ieee.org/document/6606589 for more info.
"""
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.contributors_count import ContributorsCount
from pydriller.metrics.process.contributors_experience import ContributorsExperience
from pydriller.metrics.process.history_complexity import HistoryComplexity
from pydriller.metrics.process.hunks_count import HunksCount
from pydriller.metrics.process.lines_count import LinesCount

def commits_count(path_to_repo: str, from_commit: str = None, to_commit: str = None):
    return CommitsCount(path_to_repo,
                        from_commit=from_commit,
                        to_commit=to_commit).count()

def contributors_count(path_to_repo: str, from_commit: str = None, to_commit: str = None):
    return ContributorsCount(path_to_repo,
                             from_commit=from_commit,
                             to_commit=to_commit).count()

def highest_contributors_experience(path_to_repo: str, from_commit: str = None, to_commit: str = None):
    return ContributorsExperience(path_to_repo,
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

def lines_count(path_to_repo: str, from_commit: str = None, to_commit: str = None):
    return LinesCount(path_to_repo,
                                from_commit=from_commit,
                                to_commit=to_commit).count()
