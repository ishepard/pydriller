from pydriller.metrics.process.process_metrics import ProcessMetrics

def test_to_commit_remote_1():
    count = ProcessMetrics().normalized_deleted_lines(path_to_repo='https://github.com/ishepard/pydriller',
                                                    filepath='README.md',
                                                    to_commit='772c636bb098eaba6adbafe301ce69d5f25c2c7a')
    assert count == float(0)

def test_to_commit_remote_2():
    count = ProcessMetrics().normalized_deleted_lines(path_to_repo='https://github.com/ishepard/pydriller',
                                                    filepath='README.md',
                                                    to_commit='a51a8451005781ef63bdb8946eb5d88a11eae37b')
    assert count == float(1/176)

def test_to_commit_remote_3():
    count = ProcessMetrics().normalized_deleted_lines(path_to_repo='https://github.com/ishepard/pydriller',
                                                    filepath='README.md',
                                                    to_commit='607a0b7373d9e63559fa637e357fdb48d9641fbf')
    assert count == float(1)

def test_from_commit_remote():
    count = ProcessMetrics().normalized_deleted_lines(path_to_repo='https://github.com/ishepard/pydriller',
                                                    filepath='README.md',
                                                    from_commit='cd15ee0c99a9b1f77341849670e9aece3ca34251',
                                                    to_commit='607a0b7373d9e63559fa637e357fdb48d9641fbf')
    assert count == float(1)