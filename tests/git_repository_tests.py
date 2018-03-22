import unittest
from scm.git_repository import GitRepository
from domain.change_set import ChangeSet
from datetime import datetime
from dateutil import tz

class GitRepositoryTests(unittest.TestCase):
    def test_get_head(self):
        gr = GitRepository('../test-repos/test1/')
        self.assertIsNotNone(gr)
        cs = gr.get_head()
        self.assertIsNotNone(cs)

        self.assertEqual(cs.id, '09f6182cef737db02a085e1d018963c7a29bde5a')
        self.assertEqual(1521711723, cs.date.timestamp())

    def test_get_change_sets(self):
        gr = GitRepository('../test-repos/test1/')
        self.assertIsNotNone(gr)
        change_sets = gr.get_change_sets()
        tozone = tz.gettz('GMT+1')

        cs1 = ChangeSet('a88c84ddf42066611e76e6cb690144e5357d132c',
                        datetime.fromtimestamp(1521711671).replace(tzinfo=tozone))
        cs2 = ChangeSet('6411e3096dd2070438a17b225f44475136e54e3a',
                        datetime.fromtimestamp(1521711707).replace(tzinfo=tozone))
        cs3 = ChangeSet('09f6182cef737db02a085e1d018963c7a29bde5a',
                        datetime.fromtimestamp(1521711723).replace(tzinfo=tozone))

        self.assertIn(cs1, change_sets)
        self.assertIn(cs2, change_sets)
        self.assertIn(cs3, change_sets)
        self.assertEqual(3, len(change_sets))



