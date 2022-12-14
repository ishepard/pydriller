from pydriller import Repository
from datetime import datetime
# import logging

# logging.basicConfig(level=logging.INFO)

dt1 = datetime(2021, 1, 1)
dt2 = datetime(2021, 7, 1)

for commit in Repository('/Users/dspadini/Documents/pydriller/test-repos/hadoop', since=dt1, to=dt2, num_workers=10).traverse_commits():
    for mod in commit.modified_files:
        print(mod.filename)