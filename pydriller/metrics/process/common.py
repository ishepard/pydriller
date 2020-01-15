"""
Module that implements common methods for process metrics.
"""

from pydriller.repository_mining import RepositoryMining

def get_releases(path_to_repo: str, from_commit: str = None,
                 to_commit: str = None):
    """
    Return all the releases' sha of a repo between two commits sorted
    descending from latest.
    :to_commit: the SHA of the commit to stop counting. If None, the
        analysis starts from the latest commit
    :from_commit: the SHA of the commit to start counting. If None, the
        analysis ends to the first commit

    :return: set of commit hash
    """
    # Get the sha of all releases in the repo
    releases = set()
    for commit in RepositoryMining(path_to_repo,
                                   from_commit=from_commit,
                                   to_commit=to_commit,
                                   reversed_order=True,
                                   only_releases=True).traverse_commits():
        releases.add(commit.hash)

    return releases
