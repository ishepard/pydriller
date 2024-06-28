from importlib.metadata import version
import re


class GitVersion(Exception):
    def __init__(self, message):
        super().__init__(message)

class CheckGitVersion:
    def check_git_version(self):
        git_version = version("gitpython")
        version_number = re.findall(r"[0-9]+\.[0-9]+", git_version)[0]
        if float(version_number) < 2.38:
            raise GitVersion(
                f"Current gitpython version is {version('gitpython')}. \n It can be upgraded with the following command: pip install gitpython --upgrade"
            )