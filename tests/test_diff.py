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
import pytest

from pydriller import GitRepository, Modification


@pytest.fixture()
def modification(request):
    path, commit = request.param
    gr = GitRepository(path)
    yield gr.get_commit(commit).modifications[0]
    gr.clear()


@pytest.mark.parametrize('modification',
                         [("test-repos/diff", "9a985d4a12a3a12f009ef39750fd9b2187b766d1")],
                         indirect=True)
def test_extract_line_number_and_content(modification: Modification):
    added = modification.diff_parsed['added']
    deleted = modification.diff_parsed['deleted']

    assert (127, '            RevCommit root = rw.parseCommit(headId);') in deleted
    assert (128, '            rw.sort(RevSort.REVERSE);') in deleted
    assert (129, '            rw.markStart(root);') in deleted
    assert (130, '            RevCommit lastCommit = rw.next();') in deleted
    assert (131, '            throw new RuntimeException("Changing this line " + path);') in added


@pytest.mark.parametrize('modification',
                         [("test-repos/diff", "f45ee2f8976d5f018a1e4ec83eb4556a3df8b0a5")],
                         indirect=True)
def test_additions(modification: Modification):
    added = modification.diff_parsed['added']
    deleted = modification.diff_parsed['deleted']

    assert (127, '            RevCommit root = rw.parseCommit(headId);') in added
    assert (128, '            rw.sort(RevSort.REVERSE);') in added
    assert (129, '            rw.markStart(root);') in added
    assert (130, '            RevCommit lastCommit = rw.next();') in added
    assert (131, '') in added
    assert len(deleted) == 0
    assert len(added) == 5


@pytest.mark.parametrize('modification',
                         [("test-repos/diff", "147c7ce9f725a0e259d63f0bf4e6c8ac085ff8c8")],
                         indirect=True)
def test_deletions(modification: Modification):
    added = modification.diff_parsed['added']
    deleted = modification.diff_parsed['deleted']

    assert (184, '            List<ChangeSet> allCs = new ArrayList<>();') in deleted
    assert (221, '    private GregorianCalendar convertToDate(RevCommit revCommit) {') in deleted
    assert (222, '        GregorianCalendar date = new GregorianCalendar();') in deleted
    assert (223, '        date.setTimeZone(revCommit.getAuthorIdent().getTimeZone());') in deleted
    assert (224, '        date.setTime(revCommit.getAuthorIdent().getWhen());') in deleted
    assert (225, '') in deleted
    assert (226, '        return date;') in deleted
    assert (227, '    }') in deleted
    assert (228, '') in deleted
    assert (301, '        if(!collectConfig.isCollectingBranches())') in deleted
    assert (302, '            return new HashSet<>();') in deleted
    assert (303, '') in deleted
    assert len(deleted) == 12
    assert len(added) == 0


@pytest.mark.parametrize('modification',
                         [("test-repos/no_newline", "52a78c1ee5d100528eccba0a3d67371dbd22d898")],
                         indirect=True)
def test_diff_no_newline(modification: Modification):
    """
    If a file ends without a newline git represents this with the additional line
        \\ No newline at end of file
    in diffs. This test asserts these additional lines are parsed correctly.
    """
    added = modification.diff_parsed['added']
    deleted = modification.diff_parsed['deleted']

    assert (1, 'test1') in deleted  # is considered as deleted as a 'newline' command is added
    assert (1, 'test1') in added  # now with added 'newline'
    assert (2, 'test2') in added
