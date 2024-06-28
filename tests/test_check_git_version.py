from pydriller.utils.check_git_version import CheckGitVersion, GitVersion
from pytest_mock import MockerFixture
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
def test_extracts_correct_version(mocker: MockerFixture, version_number, expectation):
    mocker.patch(
        "pydriller.utils.check_git_version.version",
        return_value=version_number,
    )
    with expectation:
        CheckGitVersion().check_git_version()
