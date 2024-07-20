from unittest.mock import patch
from pydriller.utils.check_git_version import CheckGitVersion, GitVersion
from contextlib import nullcontext as does_not_raise

import pytest


@pytest.mark.parametrize(
    "version_number,expectation",
    [
        ("3.2.0", does_not_raise()),
        ("2.38.1", does_not_raise()),
        ("2.0.0", pytest.raises(GitVersion)),
    ],
)
def test_extracts_correct_version(version_number, expectation):
    with patch(
        "pydriller.utils.check_git_version.subprocess.check_output"
    ) as mock_git_version:
        mock_git_version().decode.return_value.strip.return_value = (
            f"git version {version_number}"
        )
        with expectation:
            CheckGitVersion().check_git_version()
