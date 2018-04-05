from pydriller import RepositoryMining

for commit in RepositoryMining('../test-repos/test1/').traverse_commits():
    for modification in commit.modifications:
        print('Filename {}'.format(modification.filename))
        print('Diff: {}'.format(modification.diff))
