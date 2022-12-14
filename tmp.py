from pydriller import Repository
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

dt1 = datetime(2021, 1, 1)
dt2 = datetime(2021, 7, 1)

start = datetime.now()
for commit in Repository('/Users/dspadini/Documents/pydriller/test-repos/hadoop', num_workers=20).traverse_commits():
    for mod in commit.modified_files:
        a = mod.filename

end = datetime.now()

print(f"completed in {end - start}")