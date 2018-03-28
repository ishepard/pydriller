import unittest

from domain.commit import Commit
from repository_mining import RepositoryMining
from scm.commit_visitor import CommitVisitor
from scm.git_repository import GitRepository
from scm.persistence_mechanism import PersistenceMechanism
from datetime import datetime
from dateutil import tz


class RepositoryMiningTests(unittest.TestCase):
    def test_no_filters(self):
        mv = MyVisitor()
        rp = RepositoryMining('../test-repos/test1/', mv)
        rp.mine()
        lc = mv.list_commits
        self.assertEqual(5, len(lc))

    def test_since_filter(self):
        mv = MyVisitor()
        to_zone = tz.gettz('GMT+1')
        dt = datetime(2018, 3, 22, 10, 41, 30, tzinfo=to_zone)
        rp = RepositoryMining('../test-repos/test1/', mv, since=dt)
        rp.mine()
        lc = mv.list_commits
        self.assertEqual(4, len(lc))

    def test_to_filter(self):
        mv = MyVisitor()
        to_zone = tz.gettz('GMT+1')
        dt = datetime(2018, 3, 22, 10, 42, 3, tzinfo=to_zone)
        rp = RepositoryMining('../test-repos/test1/', mv, to=dt)
        rp.mine()
        lc = mv.list_commits
        self.assertEqual(3, len(lc))

    def test_since_and_to_filters(self):
        mv = MyVisitor()
        to_zone = tz.gettz('GMT+1')
        since_dt = datetime(2018, 3, 22, 10, 41, 45, tzinfo=to_zone)
        to_zone = tz.gettz('GMT+2')
        to_dt = datetime(2018, 3, 27, 17, 20, 3, tzinfo=to_zone)
        rp = RepositoryMining('../test-repos/test1/', mv, since=since_dt, to=to_dt)
        rp.mine()
        lc = mv.list_commits
        self.assertEqual(3, len(lc))

    def test_from_commit_filter(self):
        mv = MyVisitor()
        from_commit = '6411e3096dd2070438a17b225f44475136e54e3a'
        rp = RepositoryMining('../test-repos/test1/', mv, from_commit=from_commit)
        rp.mine()
        lc = mv.list_commits
        self.assertEqual(4, len(lc))

    def test_to_commit_filter(self):
        mv = MyVisitor()
        to_commit = '09f6182cef737db02a085e1d018963c7a29bde5a'
        rp = RepositoryMining('../test-repos/test1/', mv, from_commit=to_commit)
        rp.mine()
        lc = mv.list_commits
        self.assertEqual(3, len(lc))

    def test_from_and_to_commit_filters(self):
        mv = MyVisitor()
        from_commit = '6411e3096dd2070438a17b225f44475136e54e3a'
        to_commit = '09f6182cef737db02a085e1d018963c7a29bde5a'
        rp = RepositoryMining('../test-repos/test1/', mv, from_commit=from_commit, to_commit=to_commit)
        rp.mine()
        lc = mv.list_commits
        self.assertEqual(2, len(lc))

    def test_from_tag_filter(self):
        mv = MyVisitor()
        from_tag = 'v1.4'
        rp = RepositoryMining('../test-repos/test1/', mv, from_tag=from_tag)
        rp.mine()
        lc = mv.list_commits
        self.assertEqual(3, len(lc))

    def test_multiple_filters_exceptions(self):
        mv = MyVisitor()
        to_zone = tz.gettz('GMT+1')
        since_dt = datetime(2018, 3, 22, 10, 41, 45, tzinfo=to_zone)
        from_commit = '6411e3096dd2070438a17b225f44475136e54e3a'
        from_tag = 'v1.4'

        with self.assertRaises(Exception):
            RepositoryMining('../test-repos/test1/', mv, from_commit=from_commit, from_tag=from_tag)

        with self.assertRaises(Exception):
            RepositoryMining('../test-repos/test1/', mv, since=since_dt, from_commit=from_commit)

        with self.assertRaises(Exception):
            RepositoryMining('../test-repos/test1/', mv, since=since_dt, from_tag=from_tag)

        with self.assertRaises(Exception):
            RepositoryMining('../test-repos/test1/', mv, to=since_dt, to_tag=from_tag)


class MyVisitor(CommitVisitor):
    def __init__(self):
        self.list_commits = []

    def process(self, repo: GitRepository, commit: Commit, writer: PersistenceMechanism):
        self.list_commits.append(commit)