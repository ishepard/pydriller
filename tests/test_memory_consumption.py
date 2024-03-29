# Copyright 2018 Davide Spadini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import platform
import sys
import psutil
from git import Repo
from pydriller import Repository
from datetime import datetime

logging.basicConfig(level=logging.WARNING)
PATH = os.getenv('GITHUB_WORKSPACE')


def clone_temp_repo(tmpdir) -> str:
    repo_folder = tmpdir.join("pydriller")
    Repo.clone_from(url="https://github.com/ishepard/pydriller.git", to_path=repo_folder)
    return str(repo_folder)


def test_memory(caplog, tmpdir):
    if not PATH:
        # Check we are on GitHub
        return

    caplog.set_level(logging.WARNING)

    repo_folder = clone_temp_repo(tmpdir)

    logging.warning("Starting with nothing...")
    diff_with_nothing, all_commits_with_nothing = mine(repo_folder, 0)

    logging.warning("Starting with everything...")
    diff_with_everything, all_commits_with_everything = mine(repo_folder, 1)

    logging.warning("Starting with metrics...")
    diff_with_metrics, all_commits_with_metrics = mine(repo_folder, 2)

    max_values = [max(all_commits_with_nothing),
                  max(all_commits_with_everything),
                  max(all_commits_with_metrics)]
    logging.warning("Max values are: {}".format(max_values))

    minutes_with_everything = (diff_with_everything.seconds % 3600) // 60
    minutes_with_metrics = (diff_with_metrics.seconds % 3600) // 60

    logging.warning(
        "TIME: With nothing: {}:{}:{} ({} commits/sec), "
        "with everything: {}:{}:{}  ({} commits/sec), "
        "with metrics: {}:{}:{}  ({} commits/sec)".format(
            diff_with_nothing.seconds // 3600,
            (diff_with_nothing.seconds % 3600) // 60,
            diff_with_nothing.seconds % 60,
            704 // diff_with_nothing.seconds if diff_with_nothing.seconds != 0 else 0,
            diff_with_everything.seconds // 3600,
            (diff_with_everything.seconds % 3600) // 60,
            diff_with_everything.seconds % 60,
            704 // diff_with_everything.seconds,
            diff_with_metrics.seconds // 3600,
            (diff_with_metrics.seconds % 3600) // 60,
            diff_with_metrics.seconds % 60,
            704 // diff_with_metrics.seconds
        )
    )

    if any(val > 250 for val in max_values) or \
            minutes_with_everything >= 1 or \
            minutes_with_metrics >= 2:
        # if to analyze ~1000 commits requires more than 250MB of RAM,
        # more than 1 minute without metrics or
        # 2 minutes with metrics, print it
        log(diff_with_nothing, all_commits_with_nothing,
            diff_with_everything, all_commits_with_everything,
            diff_with_metrics, all_commits_with_metrics)
        raise Exception("Memory usage is too high, or it required too long to analyze all commits!")

    assert 704 == len(all_commits_with_nothing) == len(all_commits_with_everything) == len(all_commits_with_metrics)


def log(diff_with_nothing, all_commits_with_nothing,
        diff_with_everything, all_commits_with_everything,
        diff_with_metrics, all_commits_with_metrics):
    text = "*PYTHON V{}.{} - System: {}*\n" \
           "*Max memory (MB)*\n" \
           "With nothing: {}, with everything: {}, with metrics: {}\n" \
           "*Min memory (MB)*\n" \
           "With nothing: {}, with everything: {}, with metrics: {} \n" \
           "*Time*\n" \
           "With nothing: {}:{}:{}, with everything: {}:{}:{}, with metrics: {}:{}:{} \n" \
           "*Total number of commits*: {}\n" \
           "*Commits per second:*\n" \
           "With nothing: {}, with everything: {}, with metrics: {}"

    print(text.format(
        sys.version_info[0], sys.version_info[1], platform.system(),
        max(all_commits_with_nothing), max(all_commits_with_everything), max(all_commits_with_metrics),
        min(all_commits_with_nothing), min(all_commits_with_everything), min(all_commits_with_metrics),
        diff_with_nothing.seconds // 3600, (diff_with_nothing.seconds % 3600) // 60, diff_with_nothing.seconds % 60,
        diff_with_everything.seconds // 3600, (diff_with_everything.seconds % 3600) // 60,
        diff_with_everything.seconds % 60,
        diff_with_metrics.seconds // 3600, (diff_with_metrics.seconds % 3600) // 60, diff_with_metrics.seconds % 60,
        len(all_commits_with_nothing),
        len(all_commits_with_nothing) / diff_with_nothing.seconds if diff_with_nothing.seconds > 0 else len(all_commits_with_nothing),
        len(all_commits_with_everything) / diff_with_everything.seconds,
        len(all_commits_with_metrics) / diff_with_metrics.seconds
    ))


def mine(repo, _type):
    p = psutil.Process(os.getpid())
    dt2 = datetime(2021, 12, 1)
    all_commits = []

    start = datetime.now()
    for commit in Repository(repo, to=dt2).traverse_commits():
        memory = p.memory_info()[0] / (2 ** 20)
        all_commits.append(memory)

        h = commit.author.name  # noqa

        if _type == 0:
            continue

        for mod in commit.modified_files:
            dd = mod.diff  # noqa

            if _type == 1:
                continue

            if mod.filename.endswith('.py'):
                cc = mod.complexity  # noqa

    end = datetime.now()

    diff = end - start

    return diff, all_commits
