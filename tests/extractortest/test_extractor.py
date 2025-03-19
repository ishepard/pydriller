# tests/test_extractor.py
import pytest
import os

from tests.security_analysis.diff_extractor import extract_security_diffs_and_store

@pytest.mark.parametrize("repo_url", [
    "C:/Users/yara9/OneDrive/Skrivbord/DVWA",
])
def test_extract_security_diffs_and_store(repo_url, tmp_path):
    """
    A basic test that calls extract_security_diffs_and_store with a known small repo.
    Then checks if the CSV/JSON/MD files are generated.
    """
    # You might mock or just rely on a real small repo
    # For demonstration, let's just do a short check

    # By default, it writes to 'report.csv', 'report.json', 'report.md'
    extract_security_diffs_and_store(repo_url, continuous=False, interval=1)

    # Now check existence:
    assert os.path.exists("report.csv"), "report.csv not created"
    assert os.path.exists("report.json"), "report.json not created"
    assert os.path.exists("report.md"),   "report.md not created"
