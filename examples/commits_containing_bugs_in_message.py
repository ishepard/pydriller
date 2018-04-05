from pydriller import RepositoryMining

count = 0
for commit in RepositoryMining('../test-repos/test1/').traverse_commits():
    if 'bug' in commit.msg:
        print('Commit {} fixed a bug'.format(commit.hash))
        count += 1