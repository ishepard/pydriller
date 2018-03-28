import pytest
from scm.git_repository import GitRepository
from domain.change_set import ChangeSet
from datetime import datetime
from dateutil import tz


def test_get_head():
    gr = GitRepository('test-repos/test1/')
    assert gr is not None
    cs = gr.get_head()
    assert cs is not None

    assert cs.id == 'da39b1326dbc2edfe518b90672734a08f3c13458'
    assert 1522164679 == cs.date.timestamp()


def test_get_change_sets():
    gr = GitRepository('test-repos/test1/')
    assert gr is not None
    change_sets = gr.get_change_sets()
    to_zone = tz.gettz('GMT+1')

    cs1 = ChangeSet('a88c84ddf42066611e76e6cb690144e5357d132c',
                    datetime(2018, 3, 22, 10, 41, 11, tzinfo=to_zone))
    cs2 = ChangeSet('6411e3096dd2070438a17b225f44475136e54e3a',
                    datetime(2018, 3, 22, 10, 41, 47, tzinfo=to_zone))
    cs3 = ChangeSet('09f6182cef737db02a085e1d018963c7a29bde5a',
                    datetime(2018, 3, 22, 10, 42, 3, tzinfo=to_zone))
    to_zone = tz.gettz('GMT+2')
    cs4 = ChangeSet('1f99848edadfffa903b8ba1286a935f1b92b2845',
                    datetime(2018, 3, 27, 17, 10, 52, tzinfo=to_zone))

    assert cs1 in change_sets
    assert cs2 in change_sets
    assert cs3 in change_sets
    assert cs4 in change_sets
    assert 5 == len(change_sets)


def test_get_commit():
    gr = GitRepository('test-repos/test1/')
    c = gr.get_commit('09f6182cef737db02a085e1d018963c7a29bde5a')
    to_zone = tz.gettz('GMT+1')

    assert '09f6182cef737db02a085e1d018963c7a29bde5a' == c.hash
    assert 'ishepard' == c.author.name
    assert 'ishepard' == c.committer.name
    assert datetime(2018, 3, 22, 10, 42, 3, tzinfo=to_zone).timestamp() == c.date.timestamp()
    assert 1 == len(c.modifications)
    assert 'Ooops file2' == c.msg
    assert c.in_main_branch is True


def test_get_first_commit():
    gr = GitRepository('test-repos/test1/')
    c = gr.get_commit('a88c84ddf42066611e76e6cb690144e5357d132c')
    to_zone = tz.gettz('GMT+1')

    assert 'a88c84ddf42066611e76e6cb690144e5357d132c' == c.hash
    assert 'ishepard' == c.author.name
    assert 'ishepard' == c.committer.name
    assert datetime(2018,3,22,10,41,11,tzinfo=to_zone).timestamp() == c.date.timestamp()
    assert 2 == len(c.modifications)
    assert 'First commit adding 2 files' == c.msg
    assert c.in_main_branch is True


def test_checkout():
    # TODO: fix checkout
    gr = GitRepository('test-repos/test1/')
    gr.checkout('master')


def test_files():
    gr = GitRepository('test-repos/test2/')
    all = gr.files()

    assert 8 == len(all)
    assert 'test-repos/test2/tmp1.py' in all
    assert 'test-repos/test2/tmp2.py' in all
    assert 'test-repos/test2/fold1/tmp3.py' in all
    assert 'test-repos/test2/fold1/tmp4.py' in all
    assert 'test-repos/test2/fold2/tmp5.py' in all
    assert 'test-repos/test2/fold2/tmp6.py' in all
    assert 'test-repos/test2/fold2/fold3/tmp7.py' in all
    assert 'test-repos/test2/fold2/fold3/tmp8.py' in all


def test_total_commits():
    gr = GitRepository('test-repos/test1/')
    assert 5 == gr.total_commits()


def test_get_commit_from_tag():
    gr = GitRepository('test-repos/test1/')

    commit = gr.get_commit_from_tag('v1.4')

    assert '09f6182cef737db02a085e1d018963c7a29bde5a' == commit.hash
    with pytest.raises(IndexError):
        gr.get_commit_from_tag('v1.5')


def test_branches():
    gr = GitRepository('test-repos/test3/')

    commit = gr.get_commit('8cdf925bde3be3a21490d75686116b88b8263e82')
    assert commit.in_main_branch is False

    commit = gr.get_commit('189988aa490b0e5f14ed0ecb155e0e2901425d05')
    assert commit.in_main_branch is True

    commit = gr.get_commit('17bfb3f02331a7ce770e0a6b90584cdd473c6993')
    assert commit.in_main_branch is True

    commit = gr.get_commit('b5c103c7f61d05b9a35364f1923ceacc9afe7ed9')
    assert commit.in_main_branch is True
    assert commit.merge is True
