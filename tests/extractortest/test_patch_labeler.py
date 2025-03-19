import os
import pytest
from tests.security_analysis.patch_labeler import label_patches_with_commit_hash

def test_label_patches_creates_file(tmp_path, monkeypatch):
    """
    Test that label_patches_with_commit_hash creates a patch file with the expected content.
    """
    # Set the working directory to the temporary path.
    monkeypatch.chdir(tmp_path)

    # Define sample inputs.
    commit_hash = "abcdef1234567890"
    filename = "subdir/example.txt"
    diff_text = "This is a sample diff."

    # Call the function.
    label_patches_with_commit_hash(commit_hash, filename, diff_text)

    # Expected file name: first 7 characters of commit hash, with slashes replaced by underscores.
    expected_filename = f"{commit_hash[:7]}_{filename.replace('/', '_')}.diff"
    expected_path = tmp_path / "patches" / expected_filename

    # Check that the file exists and its contents match.
    assert expected_path.exists(), f"Expected file {expected_path} was not created."
    with open(expected_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == diff_text, "The patch file content does not match the expected diff text."
