.. _modifications_toplevel:

=============
Modifications
=============

You can get the list of modified files, as well as their diffs and current source code. To that, all you have to do is to get the list of *Modifications* that exists inside Commit. A modification object has the following fields:

* *old_path*: old path of the file (can be _None_ if the file is added)
* *new_path*: new path of the file (can be null if the file is deleted)
* *change_type*: type of the change 
* *diff*: diff of the change
* *source_code*: source code of the file (can be null if the file is deleted)
* *added*: number of lines added
* *removed*: number of lines removed
* *filename*: filename

For example::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        for m in commit.modifications:
            print(
                "Author {}".format(commit.author.name),
                " modified {}".format(m.filename),
                " with a change type of {}".format(m.change_type.name)
            )

