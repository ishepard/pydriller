# tests/extractortest/test_patch_labeler.py

import os
import pytest
from tests.security_analysis.patch_labeler import label_patches_with_commit_hash

def test_label_patches_with_commit_hash(tmp_path):
    """
    Ensure that label_patches_with_commit_hash creates the correct .diff file
    with the expected content.
    """
    commit_hash = "abcdef1234567890"
    filename = "my_script.py"
    diff_text = "some diff lines..."

    # Change to tmp_path so the 'patches' folder is created there
    os.chdir(tmp_path)

    label_patches_with_commit_hash(commit_hash, filename, diff_text)

    # The function shortens commit_hash to first 7 chars => 'abcdef1'
    # and replaces any slashes in filename with '_'.
    expected_filename = os.path.join(
        tmp_path,
        "patches",
        "abcdef1_my_script.py.diff"
    )
    assert os.path.exists(expected_filename), f"Patch file not found: {expected_filename}"

    with open(expected_filename, "r", encoding="utf-8") as f:
        contents = f.read()
        assert contents == diff_text, "File content does not match the provided diff_text."
