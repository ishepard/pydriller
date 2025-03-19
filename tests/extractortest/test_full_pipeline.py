# tests/extractortest/test_full_pipeline.py

import os
import subprocess
import pytest

@pytest.mark.integration
def test_full_pipeline(tmp_path):
    """
    Integration test: runs diff_extractor.py as a module via subprocess,
    verifying end-to-end functionality. This test assumes that the package structure
    is that 'tests.security_analysis.diff_extractor' is the module to run.
    """
    # Adjust to your local/test repo path. This should be a valid local Git repository.
    repo_path = r"C:\Users\yara9\OneDrive\Skrivbord\DVWA"

    # Change the current working directory to the temporary path so that
    # all output files (e.g., report.csv, report.json, report.md) are generated there.
    os.chdir(tmp_path)

    # Build the command using the correct module path.
    cmd = [
        "python",
        "-m",
        "tests.security_analysis.diff_extractor",  # Updated module path!
        "--repo", repo_path,
        "--since", "2023-01-01",
        "--to", "2023-12-31",
    ]

    # Run the command, capturing stdout and stderr.
    result = subprocess.run(cmd, capture_output=True, text=True)

    # If the command fails, report the error details.
    if result.returncode != 0:
        pytest.fail(
            f"Full pipeline test failed.\nSTDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"
        )

    # Check that the output report files are created.
    for filename in ["report.csv", "report.json", "report.md"]:
        assert os.path.exists(filename), f"{filename} was not created by the full pipeline."

    # Optionally, if any high-risk commits were flagged, ensure that the patches folder was created.
    if "High-risk commit detected" in result.stdout or "⚠" in result.stdout:
        assert os.path.isdir("patches"), "patches folder not found despite flagged commits."
