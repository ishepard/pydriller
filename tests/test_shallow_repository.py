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
from git.exc import GitCommandError
from git.objects.commit import Commit as GitCommit

from pydriller import Git, ShallowRepositoryError


@pytest.fixture
def repo(request):
    gr = Git(request.param)
    yield gr
    gr.clear()


@pytest.mark.parametrize('repo', ['test-repos/shallow_repo/'], indirect=True)
def test_shallow_clone_raises_informative_error(repo: Git):
    commit = repo.get_head()

    with pytest.raises(ShallowRepositoryError) as exc_info:
        _ = commit.modified_files

    assert "shallow clone" in str(exc_info.value)
    assert commit.hash in str(exc_info.value)


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_complete_clone_is_not_affected(repo: Git):
    modified_files = repo.get_head().modified_files

    assert [mod.filename for mod in modified_files] == ["file4.java"]


@pytest.mark.parametrize('repo', ['test-repos/small_repo/'], indirect=True)
def test_other_git_errors_are_not_relabelled(repo: Git, monkeypatch):
    commit = repo.get_head()

    def boom(*args, **kwargs):
        raise GitCommandError(["git", "diff-tree"], 128, b"fatal: something else entirely")

    monkeypatch.setattr(GitCommit, "diff", boom)

    with pytest.raises(GitCommandError) as exc_info:
        _ = commit.modified_files

    assert not isinstance(exc_info.value, ShallowRepositoryError)
    assert "something else entirely" in str(exc_info.value)
