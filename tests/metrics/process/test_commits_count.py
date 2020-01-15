import unittest
from parameterized import parameterized_class
from pydriller.metrics.process.commit_count import CommitCount

@parameterized_class([
   {'path_to_repo': 'test-repos/git-1', 'filepath': 'Arquivo.java', 'from_commit': None, 'to_commit': 'ffccf1e7497eb8136fd66ed5e42bef29677c4b71', 'release_scope': False, 'expected': 0},
   {'path_to_repo': 'test-repos/git-1', 'filepath': 'Matricula.java', 'from_commit': None, 'to_commit': 'ffccf1e7497eb8136fd66ed5e42bef29677c4b71', 'release_scope': False, 'expected': 2},
   {'path_to_repo': 'test-repos/git-1', 'filepath': 'unexisting.java', 'from_commit': None, 'to_commit': None, 'release_scope': False, 'expected': 0},
   {'path_to_repo': 'test-repos/git-1', 'filepath': 'Matricula.java', 'from_commit': None, 'to_commit': None, 'release_scope': False, 'expected': 6},
   {'path_to_repo': 'https://github.com/ishepard/pydriller', 'filepath': 'domain/developer.py', 'from_commit': None, 'to_commit': 'fdf671856b260aca058e6595a96a7a0fba05454b', 'release_scope': False, 'expected': 2},
   {'path_to_repo': 'https://github.com/ishepard/pydriller', 'filepath': 'domain/developer.py', 'from_commit': None, 'to_commit': 'fdf671856b260aca058e6595a96a7a0fba05454b', 'release_scope': True, 'expected': 2}
])

class TestCommitCount(unittest.TestCase):

    def test(self):
        metric = CommitCount(path_to_repo=self.path_to_repo,
                            filepath=self.filepath,
                            from_commit=self.from_commit,
                            to_commit=self.to_commit,
                            release_scope=self.release_scope)
        
        count = metric.count()
        self.assertEqual(count, self.expected, 'Test failed because expected ' + str(self.expected) + ' and got ' + str(count) +'!') 

if __name__ == "__main__":
    unittest.main()