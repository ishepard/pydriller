# tests/integration/test_full_pipeline.py

import pytest
import subprocess

@pytest.mark.integration
def test_full_pipeline(tmp_path):
    """
    Launch diff_extractor.py with sample arguments to ensure end-to-end execution.
    This requires a valid Git repo with possible security commits (like DVWA).
    """
    repo_url = "C:/Users/yara9/OneDrive/Skrivbord/DVWA"

    cmd = [
        "python",
        "-m",
        "pydriller.tests.security_analysis.diff_extractor",
        "--repo", repo_url,
        "--since", "2023-01-01",
        "--to", "2023-12-31",
        "--continuous", "False",
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Full pipeline test failed: {e}")
