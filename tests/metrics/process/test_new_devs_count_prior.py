from pydriller.metrics.process.process_metrics import ProcessMetrics

def test_new_dev_count_prior_release_to_commit():
    count = ProcessMetrics().new_dev_count_prior_release(path_to_repo='https://github.com/ishepard/pydriller', filepath='README.md', to_commit='9a0363f5b0300343ee1efedca0643c71120aba80')
    assert count == 0

    count = ProcessMetrics().new_dev_count_prior_release(path_to_repo='https://github.com/ishepard/pydriller', filepath='README.md', to_commit='424617854e48fe7138c0d58e51c196b99024f774')
    assert count == 1

def test_new_dev_count_prior_release_from_commit():
    count = ProcessMetrics().new_dev_count_prior_release(path_to_repo='https://github.com/ishepard/pydriller', filepath='README.md', from_commit='7c6dc89c846eca20fd9435ce089a83dfa35c6970', to_commit='424617854e48fe7138c0d58e51c196b99024f774')
    assert count == 2