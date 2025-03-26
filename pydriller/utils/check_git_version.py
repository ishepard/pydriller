# import subprocess
# import re
#
#
# class GitVersion(Exception):
#     def __init__(self, message):
#         super().__init__(message)
#
#
# class CheckGitVersion:
#     def check_git_version(self):
#         git_version = (
#             subprocess.check_output(["git", "--version"]).decode("ascii").strip()
#         )
#         version_number = re.findall(r"[0-9]+\.[0-9]+", git_version)[0]
#         if float(version_number) < 2.38:
#             raise GitVersion(
#                 f"Current git version is {version_number}. Minimum supported version is 2.38."
#             )
