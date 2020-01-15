import unittest
from parameterized import parameterized_class
from pydriller.metrics.process.owner_lines_count import OwnersContributedLines

@parameterized_class([
   {'path_to_repo': 'https://github.com/ishepard/pydriller', 'filepath': 'unexisting.java', 'from_commit': None, 'to_commit': '115953109b57d841ccd0952d70f8ed6703d175cd', 'expected': 0.0},
   {'path_to_repo': 'https://github.com/ishepard/pydriller', 'filepath': 'pydriller/repository_mining.py', 'from_commit': None, 'to_commit': '5a1a2b89c53a115e8087408469da04a7156ad808', 'expected': float(12/21)},
])

class TestOwnersContributedLines(unittest.TestCase):

    def test(self):
        metric = OwnersContributedLines(path_to_repo=self.path_to_repo,
                            filepath=self.filepath,
                            from_commit=self.from_commit,
                            to_commit=self.to_commit)
        
        count = metric.count()
        self.assertEqual(count, self.expected, 'Test failed because expected ' + str(self.expected) + ' and got ' + str(count) +'!')

if __name__ == "__main__":
    unittest.main()