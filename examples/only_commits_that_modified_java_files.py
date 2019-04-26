from pydriller import Repository

for commit in Repository('../test-repos/test1/', only_modifications_with_file_types=['.java']).traverse_commits():
    print('Hash {} modified a java file'.format(commit.hash))
