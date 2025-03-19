import pytest
import subprocess
import os

@pytest.mark.integration
def test_full_pipeline(tmp_path):
    """
    Launch diff_extractor.py with sample arguments to ensure end-to-end execution
    on a known small test repo that has at least one security commit.
    """
    # Suppose you have a small local test repo or a GitHub test repo.
    # For local, ensure it's a valid Git repo with a known high-risk commit.
    repo_url = "C:/Users/yara9/OneDrive/Skrivbord/DVWA"

    cmd = [
        "py",
        "-m",
        "tests.security_analysis.diff_extractor",
        "--repo", repo_url,
        "--since", "2023-01-01",
        "--to", "2023-12-31",
    ]

    # Use tmp_path as the working directory so output doesn't pollute your repo.
    current_dir = os.getcwd()
    os.chdir(tmp_path)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Full pipeline test failed: {e}")
    finally:
        os.chdir(current_dir)

    # Now check that the reports are created in tmp_path
    for report in ["report.csv", "report.json", "report.md"]:
        assert (tmp_path / report).exists(), f"{report} not found in {tmp_path}"

    # Check patches folder if you expect flagged commits
    patches_dir = tmp_path / "patches"
    # If you know for sure the test repo has at least 1 flagged commit:
    assert patches_dir.exists() and any(patches_dir.iterdir()), "No patch files created, but we expected flagged commits!"
