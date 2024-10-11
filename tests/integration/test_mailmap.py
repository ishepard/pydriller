from pydriller import Repository
from pydriller.domain.developer import Developer


PATH_TO_REPO = "test-repos/contentmine_mailmap"


def test_without_mailmap():
    sam = Developer("Sam Pablo Kuper", "sampablokuper@riseup.net")
    thomas = Developer("My Name", "tarrow@users.noreply.github.com")

    commits = list(Repository(path_to_repo=PATH_TO_REPO).traverse_commits())

    assert commits[0].author == sam
    assert commits[-1].author == thomas


def test_with_mailmap():
    sam = Developer("Sam Pablo Kuper", "sampablokuper@uclmail.net")
    thomas = Developer("Thomas Arrow", "thomasarrow@gmail.com")

    commits = list(Repository(path_to_repo=PATH_TO_REPO, use_mailmap=True).traverse_commits())

    assert commits[0].author == sam
    assert commits[-1].author == thomas
