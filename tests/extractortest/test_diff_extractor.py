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

# --- Fake classes to simulate PyDriller commit objects ---
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

# --- Tests for individual functions ---

@pytest.mark.parametrize("msg,expected_category", [
    ("Fix SQL injection vulnerability", "A03:2021 - Injection"),
    ("Improve error logging", "Unknown Category"),
])
def test_classify_owasp(msg, expected_category):
    assert classify_owasp(msg) == expected_category

@pytest.mark.parametrize("msg,expected_severity", [
    ("Fixed remote code execution bug", "Critical"),
    ("Minor patch update", "Low"),
])
def test_classify_severity(msg, expected_severity):
    assert classify_severity(msg) == expected_severity

def test_extract_cve_ids_from_msg():
    msg = "This commit references CVE-2021-1234 and also CVE-2022-5678."
    cves = extract_cve_ids_from_msg(msg)
    assert "CVE-2021-1234" in cves
    assert "CVE-2022-5678" in cves

# --- Integration tests for process_commit and save_results ---

def test_process_commit_and_save_results(tmp_path, monkeypatch):
    """
    Test process_commit() and save_results() by simulating a commit
    and verifying that report files and patch files are created in the temp folder.
    """
    # Create fake commit with one modified file.
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
    # We expect the commit to be flagged.
    assert len(flagged_commits) == 1

    # Set working directory to temporary path so reports and patches go there.
    monkeypatch.chdir(tmp_path)
    save_results(flagged_commits)

    # Check that the report files are created.
    for report in ["report.csv", "report.json", "report.md"]:
        report_path = tmp_path / report
        assert report_path.exists(), f"{report} was not created."

    # Check that a patch file was created in the "patches" folder.
    patches_dir = tmp_path / "patches"
    expected_patch = patches_dir / f"{commit.hash[:7]}_{'test.txt'.replace('/', '_')}.diff"
    assert expected_patch.exists(), "Expected patch file was not created."

    # Optionally, load and check contents of one report file (e.g., JSON).
    with open(tmp_path / "report.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # There should be one entry with the fake commit's hash.
    assert any(entry["commit_hash"] == commit.hash for entry in data), "Fake commit not found in JSON report."
