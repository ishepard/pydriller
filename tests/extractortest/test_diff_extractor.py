# tests/extractortest/test_diff_extractor.py

import os
import pytest

# Import from your diff_extractor module
from tests.security_analysis.diff_extractor import (
    classify_severity,
    classify_owasp,
    extract_cve_ids_from_msg,
    extract_security_diffs_and_store,
)

def test_classify_severity():
    """
    Simple check for severity classification based on known keywords.
    """
    assert classify_severity("Fixed buffer overflow") == "High"
    assert classify_severity("RCE vulnerability found") == "Critical"
    assert classify_severity("random text no security") == "Low"
    assert classify_severity("SQL injection discovered") == "Critical"
    assert classify_severity("Patch for cross site scripting") == "High"

def test_classify_owasp():
    """
    Simple check for OWASP classification based on known keywords.
    """
    assert classify_owasp("SQL injection discovered") == "A03:2021 - Injection"
    assert classify_owasp("Privilege escalation vulnerability") == "A06:2021 - Vulnerable & Outdated Components"
    assert classify_owasp("random commit") == "Unknown Category"
    assert classify_owasp("buffer overflow fix") == "A05:2021 - Security Misconfiguration"

def test_extract_cve_ids_from_msg():
    """
    Check CVE extraction with various patterns (case-insensitive).
    """
    msg = "Fix CVE-2023-1234 and mention cve-2019-0001 as well."
    cves = extract_cve_ids_from_msg(msg)
    assert "CVE-2023-1234" in cves
    assert "cve-2019-0001".upper() in [x.upper() for x in cves]

@pytest.mark.parametrize("repo_path", [
    # Adjust path to your local or test repository
    r"C:\Users\yara9\OneDrive\Skrivbord\DVWA",
])
def test_extract_security_diffs_and_store(repo_path, tmp_path):
    """
    Unit test extract_security_diffs_and_store() in non-continuous mode,
    verifying that output files are created (CSV, JSON, MD) in a temporary folder.
    """
    # Switch to tmp_path so all outputs land there
    os.chdir(tmp_path)

    flagged_commits = extract_security_diffs_and_store(
        repo_url=repo_path,
        since=None,
        to=None,
        continuous=False,
        interval=1
    )
    # flagged_commits is a list of flagged commits (only if any matched security criteria).

    # Check for existence of summary files:
    for filename in ["report.csv", "report.json", "report.md"]:
        assert os.path.exists(filename), f"{filename} was not generated."

    # If flagged_commits is not empty, patches/ should exist with .diff files.
    if flagged_commits:
        assert os.path.isdir("patches"), "patches folder not found despite flagged commits."
