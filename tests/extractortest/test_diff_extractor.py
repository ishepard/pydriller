import os
import csv
import json
from datetime import datetime
import pytest
from tests.security_analysis.diff_extractor import (
    classify_owasp,
    classify_severity,
    extract_cve_ids_from_msg,
    process_commit,
    save_results,
)

# --- Fake classes to simulate minimal PyDriller commit objects ---
class FakeModifiedFile:
    def __init__(self, filename, diff):
        self.filename = filename
        self.diff = diff

class FakeAuthor:
    def __init__(self, name):
        self.name = name

class FakeCommit:
    def __init__(self, hash, msg, author, author_date, modified_files):
        self.hash = hash
        self.msg = msg
        self.author = author
        self.author_date = author_date
        self.modified_files = modified_files

# ---------------------------
# 1) Classification Unit Tests
# ---------------------------

@pytest.mark.parametrize("msg,expected_category", [
    ("Fix SQL injection vulnerability", "A03:2021 - Injection"),
    ("Improve error logging", "Unknown Category"),
    ("Buffer overflow fix", "A05:2021 - Security Misconfiguration"),
    ("Broken Access Control patched", "A01:2021 - Broken Access Control"),
])
def test_classify_owasp(msg, expected_category):
    assert classify_owasp(msg) == expected_category

@pytest.mark.parametrize("msg,expected_severity", [
    ("Fixed remote code execution bug", "Critical"),
    ("Minor patch update", "Low"),
    ("Privilege escalation discovered", "High"),
    ("Directory traversal fix", "Medium"),
    ("Some random text", "Low"),
])
def test_classify_severity(msg, expected_severity):
    assert classify_severity(msg) == expected_severity

def test_extract_cve_ids_from_msg():
    msg = "This commit references CVE-2021-1234 and also CVE-2022-5678."
    cves = extract_cve_ids_from_msg(msg)
    assert "CVE-2021-1234" in cves
    assert "CVE-2022-5678" in cves
    # Make sure we only found 2, not more
    assert len(cves) == 2

# ---------------------------
# 2) Edge Cases
# ---------------------------

def test_empty_commit_message():
    """
    If the commit message is empty, no security keywords or CVE references should be found.
    """
    commit = FakeCommit(
        hash="abcdef1234",
        msg="",  # empty
        author=FakeAuthor("Bob"),
        author_date=datetime(2023, 1, 1),
        modified_files=[FakeModifiedFile("test.txt", "dummy diff")]
    )
    flagged_commits = []
    process_commit(commit, flagged_commits)
    assert len(flagged_commits) == 0, "Empty commit message should not be flagged."

def test_no_modified_files():
    """
    If there are no modified files, we won't create any patch files.
    But if the commit message indicates a high severity, it should still be flagged.
    """
    commit = FakeCommit(
        hash="abcdef5678",
        msg="Critical: remote code execution found",
        author=FakeAuthor("Alice"),
        author_date=datetime(2023, 2, 1),
        modified_files=[]  # no files changed
    )
    flagged_commits = []
    process_commit(commit, flagged_commits)
    assert len(flagged_commits) == 1, "Commit with 'Critical' keyword must be flagged even if no files changed."

def test_multiple_cve_references():
    """
    If a commit references multiple CVEs, the code typically fetches details for the first CVE found,
    but we ensure all CVEs are recognized in extract_cve_ids_from_msg.
    """
    commit = FakeCommit(
        hash="abcdef9999",
        msg="Fixing CVE-2023-1111 and CVE-2023-2222 in this patch",
        author=FakeAuthor("Dev"),
        author_date=datetime(2023, 3, 1),
        modified_files=[FakeModifiedFile("test.py", "diff line 1\n diff line 2")]
    )
    flagged_commits = []
    process_commit(commit, flagged_commits)
    assert len(flagged_commits) == 1, "Commit referencing multiple CVEs should be flagged once."
    # Check the stored CVE text
    cve_text = flagged_commits[0][2]  # cve_text is at index=2 in the tuple
    assert "CVE-2023-1111" in cve_text, "First CVE must appear in cve_text."
    # It's normal if we only store details for the first CVE (the code is designed that way).
    # But we at least confirm the commit was flagged.

def test_no_security_keywords():
    """
    If the commit has no security keywords or CVE references, it should not be flagged.
    """
    commit = FakeCommit(
        hash="abcdef0000",
        msg="Refactor code for clarity",
        author=FakeAuthor("Carol"),
        author_date=datetime(2023, 4, 1),
        modified_files=[FakeModifiedFile("refactor.txt", "some changes")]
    )
    flagged_commits = []
    process_commit(commit, flagged_commits)
    assert len(flagged_commits) == 0, "Commit with no security keywords or CVEs should not be flagged."

# ---------------------------
# 3) Integration-Like Test for process_commit + save_results
# ---------------------------

def test_process_commit_and_save_results(tmp_path, monkeypatch):
    """
    Test process_commit() + save_results() with a commit that triggers a high severity.
    We verify that patch files and reports are generated in the temp folder.
    """
    # Create fake commit with one modified file
    author = FakeAuthor("Alice")
    commit = FakeCommit(
        hash="abcdef1234567890",
        msg="Critical fix for remote code execution. CVE-2021-1234",
        author=author,
        author_date=datetime(2023, 1, 1),
        modified_files=[FakeModifiedFile("test.txt", "diff content here")]
    )
    flagged_commits = []
    process_commit(commit, flagged_commits)
    # We expect the commit to be flagged
    assert len(flagged_commits) == 1

    # Force all output into tmp_path
    monkeypatch.chdir(tmp_path)
    save_results(flagged_commits)

    # Check that the report files are created
    for report in ["report.csv", "report.json", "report.md"]:
        report_path = tmp_path / report
        assert report_path.exists(), f"{report} was not created."

    # Check that a patch file was created in the "patches" folder
    patches_dir = tmp_path / "patches"
    expected_patch = patches_dir / f"{commit.hash[:7]}_{'test.txt'.replace('/', '_')}.diff"
    assert expected_patch.exists(), "Expected patch file was not created."

    # Optionally, load & check JSON
    with open(tmp_path / "report.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert any(entry["commit_hash"] == commit.hash for entry in data), "Fake commit not found in JSON report."
