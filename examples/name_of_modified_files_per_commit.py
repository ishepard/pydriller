from pydriller import RepositoryMining

for commit in RepositoryMining('../test-repos/test1/').traverse_commits():
    print('Hash {} modified {}'.format(commit.hash, ', '.join(mod.filename for mod in commit.modifications)))
