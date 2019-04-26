from pydriller import Repository

for commit in Repository('../test-repos/test1/').traverse_commits():
    print('hash {} authored by {}'.format(commit.hash, commit.author.name))
