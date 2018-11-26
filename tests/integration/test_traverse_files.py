import logging
from datetime import datetime

import pytest

from pydriller import RepositoryMining

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def test_simple():
    list_files = RepositoryMining("test-repos/test9").traverse_files()
    assert 2 == len(list(list_files))

    # print(list_files)
