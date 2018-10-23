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
from pydriller import GitRepository


def test_extract_line_number_and_content():
    diff = "@@ -1,8 +1,8 @@\r\n" + \
           "-a\r\n" + \
           "-b\r\n" + \
           "-c\r\n" + \
           "-log.info(\"a\")\r\n" + \
           "-d\r\n" + \
           "-e\r\n" + \
           "-f\r\n" + \
           "+aa\r\n" + \
           "+bb\r\n" + \
           "+cc\r\n" + \
           "+log.info(\"aa\")\r\n" + \
           "+dd\r\n" + \
           "+ee\r\n" + \
           "+ff\r\n" + \
           " "
    gr = GitRepository('test-repos/test1')
    parsed_lines = gr.parse_diff(diff)

    added = parsed_lines['added']
    deleted = parsed_lines['deleted']

    assert (1, 'a') in deleted
    assert (2, 'b') in deleted
    assert (3, 'c') in deleted
    assert (4, 'log.info(\"a\")') in deleted
    assert (5, 'd') in deleted
    assert (6, 'e') in deleted
    assert (7, 'f') in deleted

    assert (1, 'aa') in added
    assert (2, 'bb') in added
    assert (3, 'cc') in added
    assert (4, 'log.info(\"aa\")') in added
    assert (5, 'dd') in added
    assert (6, 'ee') in added
    assert (7, 'ff') in added


def test_additions():
    diff = '@@ -2,6 +2,7 @@ aa\r\n' + \
           ' bb\r\n' + \
           ' cc\r\n' + \
           ' log.info(\"aa\")\r\n' + \
           '+log.debug(\"b\")\r\n' + \
           ' dd\r\n' + \
           ' ee\r\n' + \
           ' ff'

    gr = GitRepository('test-repos/test1')
    parsed_lines = gr.parse_diff(diff)

    added = parsed_lines['added']
    deleted = parsed_lines['deleted']

    assert (5, 'log.debug("b")') in added
    assert len(deleted) == 0
    assert len(added) == 1


def test_deletions():
    diff = '@@ -2,6 +2,7 @@ aa\r\n' + \
           ' bb\r\n' + \
           ' cc\r\n' + \
           ' log.info(\"aa\")\r\n' + \
           '-log.debug(\"b\")\r\n' + \
           ' dd\r\n' + \
           ' ee\r\n' + \
           ' ff'

    gr = GitRepository('test-repos/test1')
    parsed_lines = gr.parse_diff(diff)

    added = parsed_lines['added']
    deleted = parsed_lines['deleted']

    assert (5, 'log.debug("b")') in deleted
    assert len(deleted) == 1
    assert len(added) == 0


def test_tabs():
    diff = '@@ -1,4 +1,17 @@\r\n' + \
           ' a\r\n' + \
           ' b\r\n' + \
           '-c\r\n' + \
           '+\td\r\n' + \
           '+cc\r\n' + \
           '+\r\n' + \
           '+\r\n' + \
           '+\r\n' + \
           '+\r\n' + \
           '+\r\n' + \
           '+\r\n' + \
           '+\r\n' + \
           '+\r\n' + \
           '+\r\n' + \
           '+\tg\r\n' + \
           '+\r\n' + \
           '+j\r\n' + \
           ' '

    gr = GitRepository('test-repos/test1')
    parsed_lines = gr.parse_diff(diff)

    added = parsed_lines['added']
    deleted = parsed_lines['deleted']

    assert (3, 'c') in deleted
    assert 1 == len(deleted)

    assert (3, '\td') in added
    assert (4, 'cc') in added
    assert (5, '') in added
    assert (6, '') in added
    assert (7, '') in added
    assert (8, '') in added
    assert (9, '') in added
    assert (10, '') in added
    assert (11, '') in added
    assert (12, '') in added
    assert (13, '') in added
    assert (14, '\tg') in added
    assert (15, '') in added
    assert (16, 'j') in added
    assert 14 == len(added)


def test_real_example():
    diff = '@@ -72,7 +72,7 @@ public class GitRepository implements SCM {\r\n' + \
           ' \r\n' + \
           '        private static Logger log = Logger.getLogger(GitRepository.class);\r\n' + \
           ' \r\n' + \
           '-       public GitRepository(String path) {\r\n' + \
           '+       public GitRepository2(String path) {\r\n' + \
           '                this.path = path;\r\n' + \
           '                this.maxNumberFilesInACommit = checkMaxNumberOfFiles();\r\n' + \
           '                this.maxSizeOfDiff = checkMaxSizeOfDiff();\r\n' + \
           '@@ -155,7 +155,7 @@ public class GitRepository implements SCM {\r\n' + \
           '                return git.getRepository().getBranch();\r\n' + \
           '        }\r\n' + \
           ' \r\n' + \
           '-       public ChangeSet getHead() {\r\n' + \
           '+       public ChangeSet getHead2() {\r\n' + \
           '                Git git = null;\r\n' + \
           '                try {\r\n' + \
           '                        git = openRepository();\r\n' + \
           '@@ -320,6 +320,7 @@ public class GitRepository implements SCM {\r\n' + \
           ' \r\n' + \
           '                return diffs;\r\n' + \
           '        }\r\n' + \
           '+       newline\r\n' + \
           ' \r\n' + \
           '        private void setContext(DiffFormatter df) {\r\n' + \
           '                String context = System.getProperty(\"git.diffcontext\");'

    gr = GitRepository('test-repos/test1')
    parsed_lines = gr.parse_diff(diff)

    added = parsed_lines['added']
    deleted = parsed_lines['deleted']

    assert (75, '       public GitRepository(String path) {') in deleted
    assert (158, '       public ChangeSet getHead() {') in deleted
    assert 2 == len(deleted)

    assert (75, '       public GitRepository2(String path) {') in added
    assert (158, '       public ChangeSet getHead2() {') in added
    assert (323, '       newline') in added
    assert 3 == len(added)
