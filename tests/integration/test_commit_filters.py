import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

from repository_mining import RepositoryMining
from tests.visitor_test import VisitorTest


def test_mod_with_file_types():
    mv = VisitorTest()
    RepositoryMining('test-repos/git-4/', mv, only_modifications_with_file_types=['.java']).mine()
    lc = mv.list_commits

    assert 2 == len(lc)
    assert 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5' == lc[0].hash
    assert 'b8c2be250786975f1c6f47e96922096f1bb25e39' == lc[1].hash


def test_only_in_main_branch():
    mv = VisitorTest()
    RepositoryMining('test-repos/git-5/', mv, only_in_main_branch=True).mine()
    lc = mv.list_commits

    assert 5 == len(lc)
    assert '4a17f31c0d1285477a3a467d0bc3cb38e775097d' == lc[0].hash
    assert 'ff663cf1931a67d5e47b75fc77dcea432c728052' == lc[1].hash
    assert 'fa8217c324e7fb46c80e1ddf907f4e141449637e' == lc[2].hash
    assert '5d9d79607d7e82b6f236aa29be4ba89a28fb4f15' == lc[3].hash
    assert '377e0f474d70f6205784d0150ee0069a050c29ed' == lc[4].hash


def test_multiple_filters():
    mv = VisitorTest()
    RepositoryMining('test-repos/git-5/', mv, only_in_main_branch=True, only_no_merge=True).mine()
    lc = mv.list_commits

    assert 4 == len(lc)
    assert '4a17f31c0d1285477a3a467d0bc3cb38e775097d' == lc[0].hash
    assert 'ff663cf1931a67d5e47b75fc77dcea432c728052' == lc[1].hash
    assert 'fa8217c324e7fb46c80e1ddf907f4e141449637e' == lc[2].hash
    assert '377e0f474d70f6205784d0150ee0069a050c29ed' == lc[3].hash

def test_no_filters():
    mv = VisitorTest()
    RepositoryMining('test-repos/git-4/', mv).mine()
    lc = mv.list_commits

    assert 3 == len(lc)
    assert 'a1b6136f978644ff1d89816bc0f2bd86f6d9d7f5' == lc[0].hash
    assert '375de7a8275ecdc0b28dc8de2568f47241f443e9' == lc[1].hash
    assert 'b8c2be250786975f1c6f47e96922096f1bb25e39' == lc[2].hash