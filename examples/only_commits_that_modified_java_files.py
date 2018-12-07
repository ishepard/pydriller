from pydriller import RepositoryMining

for commit in RepositoryMining('../test-repos/test1/', only_modifications_with_file_types=['.java']).traverse_commits():
    print('Hash {} modified a java file'.format(commit.hash))
