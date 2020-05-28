# Copyright 2018 Davide Spadini and Arie van Deursen
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
import pytest

from pydriller.git_repository import GitRepository
from pydriller.domain.commit import Commit, DMMProperty


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


@pytest.fixture()
def repo():
    path = "test-repos/dmm-test-repo"
    gr = GitRepository(path)
    yield gr
    gr.clear()


# List of (commit_message, dmm_value) pairs
#
# We use unit size to exercise all the various DMM cases
UNIT_SIZE_TEST_DATA = [
    # delta high > 0, delta low = 0 -- always DMM 0.0
    ('Commit with one large method', 0.0),

    # delta high > 0, delta low > 0 -- DMM = ratio
    ('Make large larger, add small method', 0.8),

    # delta high > 0, delta low < 0 --- always DMM 0.0
    ('Make large larger, make small smaller', 0.0),

    # delta high = 0, delta low = 0 --- no delta-changes, dmm None
    ('Modify every line in large method', None),

    # delta high = 0, delta low > 0 --- always DMM 1.0
    ('Make small method a bit larger', 1.0),

    # delta high = 0, delta low < 0 --- alwyas DMM 0.0
    ('Make small smaller', 0.0),

    # delta high < 0, delta low < 0 --- DMM = ratio
    ('Make large smaller, make small smaller', 2/3),

    # delta  high < 0, delta low = 0 -- always 1.0
    ('Make large smaller', 1.0),

    # delta high < 0, delta low > 0 -- always DMM 1.0
    ('Make large smaller, make small larger', 1.0),

    # File 1: large larger; File 2: small larger -- dmm fraction
    ('Increase in one, decrease in other file', 3/4),

    # Method with unit size exactly on the border
    ('Add method with unit size on-point', 1.0),

    # Method with unit size at off point
    ('Increase unit size to risky', 0.0)
]

UNIT_COMPLEXITY_TEST_DATA = [
    # Large method, but no conditional logic
    ('Commit with one large method', 1.0),

    # Method with cyclomatic complexity exactly on the border
    ('Add method with complexity on-point', 1.0),

    # Method with cyclomatic complexity at off point
    ('Increase complexity to risky', 0.0)
]

UNIT_INTERFACING_TEST_DATA = [
    # Large method, but no parameters
    ('Commit with one large method', 1.0),

    # Adjust method with nr of paramters exactly on the border, same size
    ('Add method with interfacing on-point', None),

    # Method with nr of parameters at off point
    ('Increase interfacing to risky', 0.0)
]


def commit_by_msg(repo: GitRepository, msg: str) -> Commit:
    for commit in repo.get_list_commits():
        if commit.msg == msg:
            return commit
    raise Exception('cannot find commit with msg {}'.format(msg))


@pytest.mark.parametrize('msg,dmm', UNIT_SIZE_TEST_DATA)
def test_dmm_unit_size(repo: GitRepository, msg: str, dmm: float):
    commit = commit_by_msg(repo, msg)
    assert commit.dmm_unit_size == dmm


@pytest.mark.parametrize('msg,dmm', UNIT_COMPLEXITY_TEST_DATA)
def test_dmm_unit_complexity(repo: GitRepository, msg: str, dmm: float):
    commit = commit_by_msg(repo, msg)
    assert commit.dmm_unit_complexity == dmm


@pytest.mark.parametrize('msg,dmm', UNIT_INTERFACING_TEST_DATA)
def test_dmm_unit_interfacing(repo: GitRepository, msg: str, dmm: float):
    commit = commit_by_msg(repo, msg)
    assert commit.dmm_unit_interfacing == dmm


def test_unsupported_language(repo: GitRepository):
    # Add .md file that cannot be analyzed by Lizard
    commit = commit_by_msg(repo, 'Offer README explaining the repo purpose')
    assert commit.dmm_unit_size is None


def test_mixin_unsupported_language(repo: GitRepository):
    # Add .txt file and update (comments in) .java files
    commit = commit_by_msg(repo, 'Release under Apache 2 license')
    assert commit.dmm_unit_size is None


def test_delta_profile_modification(repo: GitRepository):
    commit = commit_by_msg(repo, 'Increase unit size to risky')
    mod = commit.modifications[0]
    assert mod._delta_risk_profile(DMMProperty.UNIT_SIZE) == (-15, 16)


def test_delta_profile_commit(repo: GitRepository):
    commit = commit_by_msg(repo, 'Increase in one, decrease in other file')

    m0 = commit.modifications[0]
    assert m0._delta_risk_profile(DMMProperty.UNIT_SIZE) == (0, 1)
    m1 = commit.modifications[1]
    assert m1._delta_risk_profile(DMMProperty.UNIT_SIZE) == (3, 0)

    assert commit._delta_risk_profile(DMMProperty.UNIT_SIZE) == (3, 1)


def test_supported_languages(repo: GitRepository):
    # Add .md file that cannot be analyzed by Lizard
    commit = commit_by_msg(repo, 'Offer README explaining the repo purpose')
    mod = commit.modifications[0]
    assert not mod.language_supported


@pytest.mark.parametrize(
    'dlo,dhi,prop', [
        (0,  0, None),
        (1,  0, 1.0),
        (-1,  0, 0.0),
        (0,  1, 0.0),
        (0, -1, 1.0),
        (1,  1, 0.5),
        (-1, -1, 0.5),
        (1, -1, 1.0),
        (-1,  1, 0.0)
    ])
def test_good_proportion(dlo: int, dhi: int, prop: float):
    assert Commit._good_change_proportion(dlo, dhi) == prop
