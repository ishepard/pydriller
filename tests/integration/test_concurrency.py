# import pytest
#
# from pydriller.repository_mining import RepositoryMining
# from pydriller.tests.integration.concurrency_visitor_test import ConcurrencyVisitorTest
#
# results = []
#
#
# def test_sequential():
#     mv = ConcurrencyVisitorTest()
#     RepositoryMining('test-repos/git-3/', mv).mine()
#     add_result(mv.visited_hashes, mv.visited_times, mv.visited_commits)
#
#
# def test_threads1():
#     mv = ConcurrencyVisitorTest()
#     RepositoryMining('test-repos/git-3/', mv, num_threads=2).mine()
#     add_result(mv.visited_hashes, mv.visited_times, mv.visited_commits)
#
#
# def test_threads2():
#     mv = ConcurrencyVisitorTest()
#     RepositoryMining('test-repos/git-3/', mv, num_threads=100).mine()
#     add_result(mv.visited_hashes, mv.visited_times, mv.visited_commits)
#
#
# def add_result(visited_hashes, visited_times, visited_commits):
#     res = dict()
#     res['visited_hashes'] = visited_hashes
#     res['visited_times'] = visited_times
#     res['visited_commits'] = visited_commits
#     results.append(res)
#
#
# def test_teardown():
#     res1 = results.pop()
#     for result in results:
#         assert res1['visited_hashes'] == result['visited_hashes']
#         assert res1['visited_times'] == result['visited_times']
#         assert res1['visited_commits'] == result['visited_commits']
