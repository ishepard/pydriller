import unittest
from parameterized import parameterized_class
from pydriller.metrics.process.devs_count import DevsCount

@parameterized_class([
   {'path_to_repo': 'test-repos/git-1', 'filepath': 'unexisting.java', 'from_commit': None, 'to_commit': 'ffccf1e7497eb8136fd66ed5e42bef29677c4b71', 'expected': (0, 0)},
   {'path_to_repo': 'test-repos/git-1', 'filepath': 'Matricula.java', 'from_commit': None, 'to_commit': 'ffccf1e7497eb8136fd66ed5e42bef29677c4b71', 'expected': (1, 1)},
   {'path_to_repo': 'https://github.com/ishepard/pydriller', 'filepath': 'pydriller/repository_mining.py', 'from_commit': None, 'to_commit': None, 'expected': (3, 1)},
   {'path_to_repo': 'https://github.com/ishepard/pydriller', 'filepath': 'domain/developer.py', 'from_commit': None, 'to_commit': '115953109b57d841ccd0952d70f8ed6703d175cd', 'expected': (1, 0)}
])

class TestDevsCount(unittest.TestCase):

    def test(self):
        metric = DevsCount(path_to_repo=self.path_to_repo,
                            filepath=self.filepath,
                            from_commit=self.from_commit,
                            to_commit=self.to_commit)
        
        count = metric.count()
        self.assertEqual(count, self.expected, 'Test failed because expected ' + str(self.expected) + ' and got ' + str(count) +'!') 

if __name__ == "__main__":
    unittest.main()