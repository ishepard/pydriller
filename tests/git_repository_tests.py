import unittest
from scm.git_repository import GitRepository
from domain.change_set import ChangeSet
from datetime import datetime
from dateutil import tz
from pprint import pprint


class GitRepositoryTests(unittest.TestCase):
    def test_get_head(self):
        gr = GitRepository('../test-repos/test1/')
        self.assertIsNotNone(gr)
        cs = gr.get_head()
        self.assertIsNotNone(cs)

        self.assertEqual(cs.id, 'da39b1326dbc2edfe518b90672734a08f3c13458')
        self.assertEqual(1522164679, cs.date.timestamp())

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
        tozone = tz.gettz('GMT+2')
        cs4 = ChangeSet('1f99848edadfffa903b8ba1286a935f1b92b2845',
                        datetime.fromtimestamp(1522163452).replace(tzinfo=tozone))

        self.assertIn(cs1, change_sets)
        self.assertIn(cs2, change_sets)
        self.assertIn(cs3, change_sets)
        self.assertIn(cs4, change_sets)
        self.assertEqual(5, len(change_sets))

    def test_get_commit(self):
        gr = GitRepository('../test-repos/test1/')
        c = gr.get_commit('09f6182cef737db02a085e1d018963c7a29bde5a')
        tozone = tz.gettz('GMT+1')

        print(c)
        self.assertEqual('09f6182cef737db02a085e1d018963c7a29bde5a', c.hash)
        self.assertEqual('ishepard', c.author.name)
        self.assertEqual('ishepard', c.committer.name)
        self.assertEqual(datetime.fromtimestamp(1521711723).replace(tzinfo=tozone).timestamp(), c.date.timestamp())
        self.assertEqual(1, len(c.modifications))
        self.assertEqual('Ooops file2', c.msg)

    def test_get_first_commit(self):
        gr = GitRepository('../test-repos/test1/')
        c = gr.get_commit('a88c84ddf42066611e76e6cb690144e5357d132c')
        print(c)
        tozone = tz.gettz('GMT+1')

    def test_checkout(self):
        gr = GitRepository('../test-repos/test1/')
        gr.checkout('master')

    def test_files(self):
        gr = GitRepository('../test-repos/test2/')
        all = gr.files()

        self.assertEqual(8, len(all))
        self.assertIn('../test-repos/test2/tmp1.py', all)
        self.assertIn('../test-repos/test2/tmp2.py', all)
        self.assertIn('../test-repos/test2/fold1/tmp3.py', all)
        self.assertIn('../test-repos/test2/fold1/tmp4.py', all)
        self.assertIn('../test-repos/test2/fold2/tmp5.py', all)
        self.assertIn('../test-repos/test2/fold2/tmp6.py', all)
        self.assertIn('../test-repos/test2/fold2/fold3/tmp7.py', all)
        self.assertIn('../test-repos/test2/fold2/fold3/tmp8.py', all)

    def test_total_commits(self):
        gr = GitRepository('../test-repos/test1/')

        self.assertEqual(5, gr.total_commits())

    def test_get_commit_from_tag(self):
        gr = GitRepository('../test-repos/test1/')

        commit = gr.get_commit_from_tag('v1.4')

        self.assertEqual('09f6182cef737db02a085e1d018963c7a29bde5a', commit)
        with self.assertRaises(IndexError):
            gr.get_commit_from_tag('v1.5')