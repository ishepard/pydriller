"""
Copyright 2016 The Chromium Authors. All rights reserved.
Use of this source code is governed by a BSD-style license that can be
found in the LICENSE file.

This is a slightly modified verion of the "git hyper-blame" found in Google
depot_tools.
See https://github.com/GiantPay/depot_tools/blob/master/git_hyper_blame.py
for more information.
"""

import collections
from datetime import datetime, timedelta, timezone
import logging

from git import Git

logger = logging.getLogger(__name__)
BlameLine = collections.namedtuple(
    'BlameLine',
    'commit context lineno_then lineno_now modified')


class HyperBlameCommit():
    """Info about a commit."""
    def __init__(self, commithash):
        self.commithash = commithash
        self.author = None
        self.author_mail = None
        self.author_time = None
        self.author_tz = None
        self.committer = None
        self.committer_mail = None
        self.committer_time = None
        self.committer_tz = None
        self.summary = None
        self.boundary = None
        self.previous = None
        self.filename = None

    def __repr__(self):  # pragma: no cover
        return '<Commit %s>' % self.commithash


class GitHyperBlame:
    def __init__(self, path: str):
        self.g = Git(path)
        self.diff_hunks_cache = {}

    def parse_blame(self, blameoutput):
        """Parses the output of git blame -p into a data structure."""
        lines = blameoutput.split('\n')
        i = 0
        commits = {}

        while i < len(lines):
            # Read a commit line and parse it.
            line = lines[i]
            i += 1
            if not line.strip():
                continue
            commitline = line.split()
            commithash = commitline[0]
            lineno_then = int(commitline[1])
            lineno_now = int(commitline[2])

            try:
                commit = commits[commithash]
            except KeyError:
                commit = HyperBlameCommit(commithash)
                commits[commithash] = commit

            # Read commit details until we find a context line.
            while i < len(lines):
                line = lines[i]
                i += 1
                if line.startswith('\t'):
                    break

                try:
                    key, value = line.split(' ', 1)
                except ValueError:
                    key = line
                    value = True
                setattr(commit, key.replace('-', '_'), value)

            context = line[1:]

            yield BlameLine(commit, context, lineno_then, lineno_now, False)

    def get_parsed_blame(self, filename, revision='HEAD'):
        blame = self.g.blame('-p', revision, '--', filename)
        return list(self.parse_blame(blame))

    def hyper_blame(self, ignored, filename, revision='HEAD'):
        # Map from commit to parsed blame from that commit.
        blame_from = {}

        def cache_blame_from(filename, commithash):
            try:
                return blame_from[commithash]
            except KeyError:
                parsed = self.get_parsed_blame(filename, commithash)
                blame_from[commithash] = parsed
                return parsed

        parsed = cache_blame_from(filename, revision)

        new_parsed = []
        for line in parsed:
            # If a line references an ignored commit, blame that commit's
            # parent repeatedly until we find a non-ignored commit.
            while line.commit.commithash in ignored:
                if line.commit.previous is None:
                    # You can't ignore the commit that added this file.
                    break

                previouscommit, previousfilename = line.commit.previous.split(
                    ' ', 1)
                parent_blame = cache_blame_from(previousfilename,
                                                previouscommit)

                if len(parent_blame) == 0:
                    # The previous version of this file was empty,
                    # therefore, you can't ignore this commit.
                    break

                # line.lineno_then is the line number in question at
                # line.commit. We need
                # to translate that line number so that it refers to the
                # position of the same line on previouscommit.
                lineno_previous = self.approx_lineno_across_revs(
                    line.commit.filename, previousfilename,
                    line.commit.commithash,
                    previouscommit, line.lineno_then)
                logger.debug('ignore commit %s on line p%d/t%d/n%d',
                             line.commit.commithash, lineno_previous,
                             line.lineno_then,
                             line.lineno_now)

                # Get the line at lineno_previous in the parent commit.
                assert 1 <= lineno_previous <= len(parent_blame)
                newline = parent_blame[lineno_previous - 1]

                # Replace the commit and lineno_then, but not the lineno_now
                # or context.
                line = BlameLine(newline.commit, line.context,
                                 newline.lineno_then,
                                 line.lineno_now, True)
                logger.debug('replacing with %r', line)

            new_parsed.append(line)

        return self.build_result(new_parsed)

    def approx_lineno_across_revs(self, filename, newfilename, revision,
                                  newrevision, lineno):
        """Computes the approximate movement of a line number between two
        revisions.

        Consider line |lineno| in |filename| at |revision|. This function
        computes the
        line number of that line in |newfilename| at |newrevision|. This is
        necessarily approximate.

        Args:
          filename: The file (within the repo) at |revision|.
          newfilename: The name of the same file at |newrevision|.
          revision: A git revision.
          newrevision: Another git revision. Note: Can be ahead or behind
          |revision|.
          lineno: Line number within |filename| at |revision|.

        Returns:
          Line number within |newfilename| at |newrevision|.
        """
        # This doesn't work that well if there are a lot of line changes
        # within the
        # hunk (demonstrated by
        # GitHyperBlameLineMotionTest.testIntraHunkLineMotion).
        # A fuzzy heuristic that takes the text of the new line and tries to
        # find a
        # deleted line within the hunk that mostly matches the new line
        # could help.

        # Use the <revision>:<filename> syntax to diff between two blobs.
        # This is the only way to diff a file that has been renamed.
        old = '%s:%s' % (revision, filename)
        new = '%s:%s' % (newrevision, newfilename)
        hunks = self.cache_diff_hunks(old, new)

        cumulative_offset = 0

        # Find the hunk containing lineno (if any).
        for (oldstart, oldlength), (newstart, newlength) in hunks:
            cumulative_offset += newlength - oldlength

            if lineno >= oldstart + oldlength:
                # Not there yet.
                continue

            if lineno < oldstart:
                # Gone too far.
                break

            # lineno is in [oldstart, oldlength] at revision; [newstart,
            # newlength] at
            # newrevision.

            # If newlength == 0, newstart will be the line before the
            # deleted hunk.
            # Since the line must have been deleted, just return that as the
            # nearest
            # line in the new file. Caution: newstart can be 0 in this case.
            if newlength == 0:
                return max(1, newstart)

            newend = newstart + newlength - 1

            # Move lineno based on the amount the entire hunk shifted.
            lineno = lineno + newstart - oldstart
            # Constrain the output within the range [newstart, newend].
            return min(newend, max(newstart, lineno))

        # Wasn't in a hunk. Figure out the line motion based on the
        # difference in
        # length between the hunks seen so far.
        return lineno + cumulative_offset

    def cache_diff_hunks(self, oldrev, newrev):
        def parse_start_length(s):
            # Chop the '-' or '+'.
            s = s[1:]
            # Length is optional (defaults to 1).
            try:
                start, length = s.split(',')
            except ValueError:
                start = s
                length = 1
            return int(start), int(length)

        try:
            return self.diff_hunks_cache[(oldrev, newrev)]
        except KeyError:
            pass

        # Use -U0 to get the smallest possible hunks.
        diff = self.g.diff(oldrev, newrev, '-U0')

        # Get all the hunks.
        hunks = []
        for line in diff.split('\n'):
            if not line.startswith('@@'):
                continue
            ranges = line.split(' ', 3)[1:3]
            ranges = tuple(parse_start_length(r) for r in ranges)
            hunks.append(ranges)

        self.diff_hunks_cache[(oldrev, newrev)] = hunks
        return hunks

    def build_result(self, parsedblame):
        table = []
        for line in parsedblame:
            offset = line.commit.author_tz
            hours = int(offset[:-2])
            minutes = int(offset[-2:])
            tz = timezone(timedelta(hours=hours, minutes=minutes))
            author_time = datetime.utcfromtimestamp(int(
                line.commit.author_time)) + timedelta(hours=hours,
                                                      minutes=minutes)
            author_time = author_time.replace(tzinfo=tz)
            row = ''
            row = [line.commit.commithash[:8],
                   '(' + line.commit.author,
                   author_time.strftime('%Y-%m-%d %H:%M:%S %z'),
                   str(line.lineno_now) + ('*' if line.modified else '') + ')',
                   line.context]
            row.insert(1, line.commit.filename)
            row = ' '.join(row)
            table.append(row)
        return table
