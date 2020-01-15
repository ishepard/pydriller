from pathlib import Path
from pydriller.metrics.process.common import get_releases

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
        self.releases = get_releases(path_to_repo=self.path_to_repo,
                                     from_commit=self.from_commit,
                                     to_commit=self.to_commit)

    def count(self):
        """
        Implement the main functionality of the metric
        """
        return 0
