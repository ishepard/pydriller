import unittest
from parameterized import parameterized_class
from pydriller.metrics.process.lines_count import NormalizedLinesCount

@parameterized_class([
   {'path_to_repo': 'https://github.com/ishepard/pydriller', 'filepath': 'README.md', 'from_commit': None, 'to_commit': '772c636bb098eaba6adbafe301ce69d5f25c2c7a', 'expected': (0, 0)},
   {'path_to_repo': 'https://github.com/ishepard/pydriller', 'filepath': 'README.md', 'from_commit': None, 'to_commit': 'bf5208c06e64153d180faf26cd9a86426631c2e4', 'expected': (float(15/246), float(7/24))},
   {'path_to_repo': 'https://github.com/ishepard/pydriller', 'filepath': 'README.md', 'from_commit': None, 'to_commit': 'e7255f596a1cde0f9f42a962969d541e5186c441', 'expected': (1, 0)},
])

class TestNormalizedLinesCount(unittest.TestCase):

    def test(self):
        metric = NormalizedLinesCount(path_to_repo=self.path_to_repo,
                                      filepath=self.filepath,
                                      from_commit=self.from_commit,
                                      to_commit=self.to_commit)
        
        count = metric.count()
        self.assertEqual(count, self.expected, 'Test failed because expected ' + str(self.expected) + ' and got ' + str(count) +'!')

if __name__ == "__main__":
    unittest.main()