from pydriller import RepositoryMining

for commit in RepositoryMining('../test-repos/test1/').traverse_commits():
    print('hash {} authored by {}'.format(commit.hash, commit.author.name))
