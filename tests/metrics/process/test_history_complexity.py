import pytest
from pydriller.metrics.process.history_complexity import HistoryComplexity, HistoryPeriod

test_data = [
    ('https://github.com/ishepard/pydriller', 'README.md', '2d96492b6b446f424d55f197f2717655077973ab', HistoryPeriod.RELEASE, (6.888, 0.3326, 0.0603)),
    ('https://github.com/ishepard/pydriller', 'README.md', '2d96492b6b446f424d55f197f2717655077973ab', HistoryPeriod.WEEK, (11.017, 0.8243, 0.2543)),
    ('https://github.com/ishepard/pydriller', 'README.md', '2d96492b6b446f424d55f197f2717655077973ab', HistoryPeriod.MONTH, (5.4096, 0.2542, 0.0212)),
    ('https://github.com/ishepard/pydriller', 'README.md', '2d96492b6b446f424d55f197f2717655077973ab', HistoryPeriod.ALL, (0.3498, 0.013, 0.0))
]

@pytest.mark.parametrize('path_to_repo, filepath, to_commit, period,  expected', test_data)
def test(path_to_repo, filepath, to_commit, period, expected):
    metric = HistoryComplexity(path_to_repo=path_to_repo,
                                    filepath=filepath,
                                    to_commit=to_commit)
    
    count = metric.count(period=period)
    assert count == expected, f'Test failed because expected {str(expected)} and got {str(count)}!'
