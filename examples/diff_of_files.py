from pydriller import Repository

for commit in Repository('../test-repos/test1/').traverse_commits():
    for modification in commit.modifications:
        print('Filename {}'.format(modification.filename))
        print('Diff: {}'.format(modification.diff))
