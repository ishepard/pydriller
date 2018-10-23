.. _commit_toplevel:

=============
Commit Object
=============

A Commit contains a hash, a committer (name and email), an author (name, and email), a message, the authored date, committed date, a list of its parent hashes (if it's a merge commit, the commit has two parents), and the list of modification. Furthermore, the commit also contains the project name.

For example::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        print(
            'Hash: {}\n'.format(commit.hash),
            'Author: {}'.format(commit.author.name),
            'Committer: {}'.format(commit.committer.name),
            'In project: {}'.format(commit.project_name),
            'Author date: {}'.format(commit.author_date.strftime("%Y-%m-%d %H:%M:%S")),
            'Message: {}'.format(commit.msg),
            'Merge: {}'.format(commit.merge),
            'In main branch: {}'.format(commit.in_main_branch)
    )
