from pydriller import RepositoryMining

for commit in RepositoryMining('../test-repos/test1/').traverse_commits():
    print('Hash {} authored by {} includes {} modified files'.format(commit.hash, commit.author.name, len(commit.modifications)))
