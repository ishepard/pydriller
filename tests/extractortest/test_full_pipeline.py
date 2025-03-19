# tests/extractortest/test_full_pipeline.py
import pytest
import subprocess

@pytest.mark.integration
def test_full_pipeline(tmp_path):
    """
    Launch diff_extractor.py with sample arguments to ensure end-to-end execution.
    This requires a valid Git repository with security commits.
    """
    repo_url = r"C:\Users\yara9\OneDrive\Skrivbord\DVWA"  # Ensure this is a valid local Git repo

    cmd = [
        "python",
        "-m",
        "tests.security_analysis.diff_extractor",  # Updated module path
        "--repo", repo_url,
        "--since", "2023-01-01",
        "--to", "2023-12-31",
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Full pipeline test failed: {e}")
