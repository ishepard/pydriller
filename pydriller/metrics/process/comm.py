from pydriller.repository_mining import RepositoryMining

class COMM():
    """
    This class is responsible to implement the process metric "Commit Count"
    Commit Count measures the number of commits made to a file.
    """

    def count(self, path_to_repo: str, commit_hash: str, filename: str):
        """
        Return the number of commits made to a file from the first commit to the one identified by commit_hash.
        
        :path_to_repo: path to a single repo
        :commit_hash: the SHA of the commit to stop counting
        :filename: the filename of the file to count for. E.g. 'doc/README.md'
        
        :return: int number of commits made to the file
        """
        count = 0

        for commit in RepositoryMining(path_to_repo).traverse_commits():            
            for modified_file in commit.modifications:
                if modified_file.filename == filename:
                    count += 1
                    break

            if commit.hash == commit_hash:
                break
      
        return count