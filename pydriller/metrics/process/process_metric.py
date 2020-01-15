from pathlib import Path
from pydriller.repository_mining import RepositoryMining

class ProcessMetric:
    """
    Abstract class to implement process metrics
    """

    def __init__(self, path_to_repo: str, filepath: str,
                 from_commit: str = None, to_commit: str = None,
                 release_scope: bool = True):
        """
        :path_to_repo: path to a single repo
        :filepath: the path to the file to count for. E.g. 'doc/README.md'
        :to_commit: the SHA of the commit to stop counting. If None, the
            analysis starts from the latest commit
        :from_commit: the SHA of the commit to start counting. If None, the
            analysis ends to the first commit
        :release_scope: if True counts only within the same release of the
            commit SHA 'to_commit'.
            if true returns the number of commits made to the file within the
            same release up to the commit identified by to_commit;
            if False returns the number of commits made to the file from the
            first commit to the one identified by to_commit.
        """
        self.path_to_repo = path_to_repo
        self.filepath = str(Path(filepath))
        self.from_commit = from_commit
        self.to_commit = to_commit
        self.release_scope = release_scope
        self.releases = self.__get_releases(path_to_repo=self.path_to_repo,
                                     from_commit=self.from_commit,
                                     to_commit=self.to_commit)

    def count(self):
        """
        Implement the main functionality of the metric
        """
        return 0

    def __get_releases(self, path_to_repo: str, from_commit: str = None,
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