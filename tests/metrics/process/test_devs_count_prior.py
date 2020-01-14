from pydriller.metrics.process.process_metrics import ProcessMetrics

def test_dev_count_prior_release_to_commit():
    count = ProcessMetrics().dev_count_prior_release(path_to_repo='https://github.com/ishepard/pydriller', filepath='README.md', to_commit='424617854e48fe7138c0d58e51c196b99024f774')
    assert count == 2

def test_dev_count_prior_release_from_commit():
    count = ProcessMetrics().dev_count_prior_release(path_to_repo='https://github.com/ishepard/pydriller', filepath='README.md', from_commit='98b377ba4d2653de5f96ca6513217d744f6d9b7b', to_commit='424617854e48fe7138c0d58e51c196b99024f774')
    assert count == 1