import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

import pytest

from domain.modification import Modification
from domain.modification_type import ModificationType


def test_should_get_adds_and_removes():

    diff = "+++ diff info\n" \
       + "+ new line\n" \
       + "- removed line\n" \
       + "+ new line\n" \
       + "\n" \
       + "+ new line\n" \
       + "- removed line\n" \
       + "+++ more git stuff\n" \
       + "--- more git stuff\n"

    m =  Modification("old", "new", ModificationType.ADD, diff, "class Java {} ");

    assert 3 == m.added
    assert 2 == m.removed


def test_should_get_name_of_file_even_when_deleted():
    m1 = Modification("/a/b/Class.java", "/dev/null", ModificationType.DELETE, "bla bla", "bla bla");
    assert "Class.java" == m1.filename

    m2 = Modification("/a/b/Class.java", "/a/b/Class.java", ModificationType.MODIFY, "bla bla", "bla bla");
    assert "Class.java" == m2.filename

    m3 = Modification("/dev/null", "/a/b/Class.java", ModificationType.ADD, "bla bla", "bla bla");
    assert "Class.java" == m3.filename
