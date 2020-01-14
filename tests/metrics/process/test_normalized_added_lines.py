from pydriller.metrics.process.process_metrics import ProcessMetrics


def test_to_commit_remote_1():
    count = ProcessMetrics().normalized_added_lines(path_to_repo='https://github.com/ishepard/pydriller',
                                                    filepath='README.md',
                                                    to_commit='772c636bb098eaba6adbafe301ce69d5f25c2c7a')
    assert count == float(0)

def test_to_commit_remote_2():
    count = ProcessMetrics().normalized_added_lines(path_to_repo='https://github.com/ishepard/pydriller',
                                                    filepath='README.md',
                                                    to_commit='bf5208c06e64153d180faf26cd9a86426631c2e4')
    assert count == float(15/246)

def test_to_commit_remote_3():
    count = ProcessMetrics().normalized_added_lines(path_to_repo='https://github.com/ishepard/pydriller',
                                                    filepath='README.md',
                                                    to_commit='e7255f596a1cde0f9f42a962969d541e5186c441')
    assert count == float(1)

def test_from_commit_remote():
    count = ProcessMetrics().normalized_added_lines(path_to_repo='https://github.com/ishepard/pydriller',
                                                    filepath='README.md',
                                                    from_commit='f3a99e137a624396cf587f04ab3ddc42044c09d3',
                                                    to_commit='bf5208c06e64153d180faf26cd9a86426631c2e4')
    assert count == float(15/86)