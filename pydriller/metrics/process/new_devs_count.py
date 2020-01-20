"""
Module that calculates the number of NEW developers that contributed to a file
"""
from pathlib import Path
from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

class NewDevsCount(ProcessMetric):
    """
    This class is responsible to implement the following metrics: \
    * New Developers Count: is the number of "new" developers who changed \
        the file in the commit release.
    """

    def count(self):
        """
        Return the distinct number of new developers who
        contributed to the file up to the indicated commit.

        A new developer contributing to a file F in release R is a developer \
        that modified F in that release but never changed it in prior releases.

        :return: int number of developers
        """
        filepath = self.filepath
        developers = set()
        duplicates = set()
        # Get the sha of all releases in the repo
        releases = set()
        for commit in RepositoryMining(self.path_to_repo,
                                       to_commit=self.to_commit,
                                       reversed_order=True,
                                       only_releases=True).traverse_commits():
            releases.add(commit.hash)

        in_prior_release = False
        in_older_release = False

        for commit in RepositoryMining(self.path_to_repo, 
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            sha = commit.hash
            if sha in releases:
                if not in_prior_release:
                    in_prior_release = True
                    # Start count from next iteration
                    continue
                else:
                    # Reached a release older than the prior
                    in_older_release = True

            if not in_prior_release:
                continue

            for modified_file in commit.modifications:

                stop_count = False

                if filepath in (modified_file.new_path,
                                modified_file.old_path):

                    author = commit.author.email.strip()

                    if in_older_release and author in developers:
                        duplicates.add(author)
                    else:
                        developers.add(author)

                    if modified_file.change_type == ModificationType.RENAME:
                        filepath = str(Path(modified_file.old_path))
                    elif modified_file.change_type == ModificationType.ADD:
                        stop_count = True

                    break

                if stop_count:
                    break

        if developers == duplicates:
            new_devs = developers
        else:
            new_devs = developers - duplicates

        return len(new_devs)
        