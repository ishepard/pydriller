from pydriller import Repository

for commit in Repository('../test-repos/test1/').traverse_commits():
    print('Hash {} authored by {} includes {} modified files'.format(commit.hash, commit.author.name, len(commit.modifications)))
