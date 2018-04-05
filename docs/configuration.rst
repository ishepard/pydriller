.. _configuration_toplevel:

=============
Configuration
=============

One of the main advantage of using PyDriller to mine software repositories, is that is highly configurable. Let's start with selecting which commit to analyze.

Selecting the Commit Range
==========================

By default, PyDriller executes the visitor for all the commits in the repository. However, filters can be applied to `RepositoryMining` to visit *only specific* commits. 

* *single: str*: single hash of the commit. The visitor will be called only on this commit

*FROM*:

* *since: datetime*: only commits after this date will be analyzed
* *from_commit: str*: only commits after this commit hash will be analyzed
* *from_tag: str*: only commits after this commit tag will be analyzed

*TO*:

* *to: datetime*: only commits up to this date will be analyzed
* *to_commit: str*: only commits up to this commit hash will be analyzed
* *to_tag: str*: only commits up to this commit tag will be analyzed

Examples::

    # Analyze single commit
    RepositoryMining('path/to/the/repo', single='6411e3096dd2070438a17b225f44475136e54e3a').traverse_commits()

    # Since 8/10/2016
    RepositoryMining('path/to/the/repo', since=datetime(2016, 10, 8, 17, 0, 0)).traverse_commits()

    # Between 2 dates
    dt1 = datetime(2016, 10, 8, 17, 0, 0)
    dt2 = datetime(2016, 10, 8, 17, 59, 0)
    RepositoryMining('path/to/the/repo', since=dt1, to=dt2).traverse_commits()

    # Between tags
    from_tag = 'tag1'
    to_tag = 'tag2'
    RepositoryMining('path/to/the/repo', from_tag=from_tag, to_tag=to_tag).traverse_commits()

    # Up to a date
    dt1 = datetime(2016, 10, 8, 17, 0, 0, tzinfo=to_zone)
    RepositoryMining('path/to/the/repo', to=dt1).traverse_commits()

    # !!!!! ERROR !!!!! THIS IS NOT POSSIBLE
    RepositoryMining('path/to/the/repo', from_tag=from_tag, from_commit=from_commit).traverse_commits()

**IMPORTANT**: it is **not** possible to configure more than one filter of the same category (for example, more than one *from*). It is also **not** possible to have the *single* filter together with other filters!


Filtering commits
=================

PyDriller comes with a set of common commit filters that you can apply:

* *only\_in\_branches: List[str]*: only visits commits that belong to certain branches.
* *only\_in\_main\_branch: bool*: only visits commits that belong to the main branch of the repository.
* *only\_no\_merge: bool*: only visits commits that are not merge commits.
* *only\_modifications\_with\_file\_types: List[str]*: only visits commits in which at least one modification was done in that file type, e.g., if you pass ".java", then, the it will visit only commits in which at least one Java file was modified; clearly, it will skip other commits.

Examples::

    # Only commits in main branch
    RepositoryMining('path/to/the/repo', only_in_main_branch=True).traverse_commits()

    # Only commits in main branch and no merges
    RepositoryMining('path/to/the/repo', only_in_main_branch=True, only_no_merge=True).traverse_commits()

    # Only commits that modified a java file
    RepositoryMining('path/to/the/repo', only_modifications_with_file_types=['.java']).traverse_commits()


Threads
=======
TODO

PyDriller can divide the work of analyzing a repository among multiple threads. If your machine has several cores, this can significantly improve performance. However, your *CommitVisitors must be thread-safe*, and your analysis must tolerate visiting commits in a relatively arbitrary order. 
By default, PyDriller uses only 1 thread.
::

    RepositoryMining('path/to/repo/', mv, num_threads=5)

