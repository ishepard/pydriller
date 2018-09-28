.. _modifications_toplevel:

=============
Modifications
=============

You can get the list of modified files, as well as their diffs and current source code. To that, all you have to do is to get the list of *Modifications* that exists inside Commit. A modification object has the following fields:

* **old_path**: old path of the file (can be _None_ if the file is added)
* **new_path**: new path of the file (can be _None_ if the file is deleted)
* **change_type**: type of the change: can be Added, Deleted, Modified, or Renamed.
* **diff**: diff of the file as Git presents it (e.g., starting with @@ xx,xx @@).
* **source_code**: source code of the file (can be _None_ if the file is deleted)
* **added**: number of lines added
* **removed**: number of lines removed
* **nloc**: Lines Of Code (LOC) of the file
* **complexity**: Cyclomatic Complexity of the file
* **token_count**: Number of Tokens of the file
* **methods**: list of methods of the file. The list might be empty if the programming language is not supported or if the file is not a source code file. 


For example::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        for m in commit.modifications:
            print(
                "Author {}".format(commit.author.name),
                " modified {}".format(m.filename),
                " with a change type of {}".format(m.change_type.name),
                " and the complexity is {}".format(m.complexity)
            )

