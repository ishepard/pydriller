.. _repository_toplevel:

============
Repository
============
`Repository` is the main class of Pydriller, responsible of returning the list of commits you want.
One of the main advantage of using PyDriller to mine software repositories is that it is highly configurable. We will now see all the options that once can pass to Repository.

Simple Scenario
===============
This is the "Hello World" of Pydriller::

    for commit in Repository("/Users/dspadini/myrepo").traverse_commits():
        print(commit.hash)

The function `traverse_commits()` of `Repository` will return the selected commits, in this simple case *all of them*.
Now let's see how we can customize `Repository`.

Selecting projects to analyze
=============================
The only required parameter of `Repository` is **path_to_repo**, which specifies the repo(s) to analyze. It must be of type `str` or `List[str]`, meaning analyze only one repository or more than one.

Furthermore, PyDriller supports both local and remote repositories: if you pass an URL, PyDriller will automatically create a temporary folder, clone the repository, run the study, and finally delete the temporary folder. 

For example, the following are all possible inputs for `Repository`::
    
    # analyze only 1 local repository
    url = "repos/pydriller/" 
    
    # analyze 2 local repositories
    url = ["repos/pydriller/", "repos/anotherrepo/"]  
    
    # analyze both local and remote
    url = ["repos/pydriller/", "https://github.com/apache/hadoop.git", "repos/anotherrepo"] 
    
    # analyze 1 remote repository
    url = "https://github.com/apache/hadoop.git" 

To keep track of what project PyDriller is analyzing, the `Commit` object has a property called **project_name**.

Selecting the Commit Range
==========================

By default, PyDriller analyzes all the commits in the repository. However, filters can be applied to `Repository` to visit *only specific* commits.

* **single** *(str)*: single hash of the commit. The visitor will be called only on this commit

*FROM*:

* **since** *(datetime)*: only commits after this date will be analyzed
* **from\_commit** *(str)*: only commits after this commit hash will be analyzed
* **from\_tag** *(str)*: only commits after this commit tag will be analyzed

*TO*:

* **to** *(datetime)*: only commits up to this date will be analyzed
* **to\_commit** *(str)*: only commits up to this commit hash will be analyzed
* **to\_tag** *(str)*: only commits up to this commit tag will be analyzed

*ORDER*:

* **order** *(str)*: one between 'date-order', 'author-date-order', 'topo-order', and 'reverse' (see `this`_ for more information). **NOTE**: By default, PyDriller returns the commits from the oldest to the newest. If you need viceversa instead (from the newest to the oldest), use "order='reverse'".

.. _this: https://git-scm.com/docs/git-rev-list#_commit_ordering

Examples::

    # Analyze single commit
    Repository('path/to/the/repo', single='6411e3096dd2070438a17b225f44475136e54e3a').traverse_commits()

    # Since 8/10/2016
    Repository('path/to/the/repo', since=datetime(2016, 10, 8, 17, 0, 0)).traverse_commits()

    # Between 2 dates
    dt1 = datetime(2016, 10, 8, 17, 0, 0)
    dt2 = datetime(2016, 10, 8, 17, 59, 0)
    Repository('path/to/the/repo', since=dt1, to=dt2).traverse_commits()

    # Between tags
    from_tag = 'tag1'
    to_tag = 'tag2'
    Repository('path/to/the/repo', from_tag=from_tag, to_tag=to_tag).traverse_commits()

    # Up to a date
    dt1 = datetime(2016, 10, 8, 17, 0, 0, tzinfo=to_zone)
    Repository('path/to/the/repo', to=dt1).traverse_commits()

    # !!!!! ERROR !!!!! THIS IS NOT POSSIBLE
    Repository('path/to/the/repo', from_tag=from_tag, from_commit=from_commit).traverse_commits()

**IMPORTANT**: it is **not** possible to configure more than one filter of the same category (for example, more than one *from*). It is also **not** possible to have the *single* filter together with other filters!


Filtering commits
=================

PyDriller comes with a set of common commit filters that you can apply:

* **only\_in\_branch** *(str)*: only analyses commits that belong to this branch.
* **only\_no\_merge** *(bool)*: only analyses commits that are not merge commits.
* **only\_authors** *(List[str])*: only analyses commits that are made by these authors. The check is made on the username, NOT the email.
* **only\_commits** *(List[str])*: only these commits will be analyzed.
* **only_releases** *(bool)*: only commits that are tagged ("release" is a term of GitHub, does not actually exist in Git)
* **filepath** *(str)*: only commits that modified this file will be analyzed.
* **only\_modifications\_with\_file\_types** *(List[str])*: only analyses commits in which **at least** one modification was done in that file type, e.g., if you pass ".java", it will visit only commits in which at least one Java file was modified; clearly, it will skip other commits (e.g., commits that did not modify Java files).

Examples::

    # Only commits in branch1
    Repository('path/to/the/repo', only_in_branch='branch1').traverse_commits()

    # Only commits in branch1 and no merges
    Repository('path/to/the/repo', only_in_branch='branch1', only_no_merge=True).traverse_commits()

    # Only commits of author "ishepard" (yeah, that's me)
    Repository('path/to/the/repo', only_authors=['ishepard']).traverse_commits()

    # Only these 3 commits
    Repository('path/to/the/repo', only_commits=['hash1', 'hash2', 'hash3']).traverse_commits()

    # Only commit that modified "Matricula.javax" 
    Repository('path/to/the/repo', filepath='Matricula.javax').traverse_commits()

    # Only commits that modified a java file
    Repository('path/to/the/repo', only_modifications_with_file_types=['.java']).traverse_commits()


Configurations
=====================

Other than filtering commits or defining date ranges, Pydriller supports the following configurations:

* **include_refs** *(bool)*: whether to include refs and HEAD in commit analysis (equivalent of adding the flag :code:`--all`).
* **include_remotes** *(bool)*: whether to include remote commits in analysis (equivalent of adding the flag :code:`--remotes`).
* **clone_repo_to** *(str)*: if the repository is a URL, Pydriller will clone it in this directory.
* **num_workers** *(int)*: number of workers (i.e., threads). By default is 1. Please note, if num_workers > 1 the commits order is not maintained.
* **histogram** *(bool)*: uses :code:`git diff --histogram` instead of the normal git. See :ref:`git-diff-algorithms`.
* **skip_whitespaces** *(bool)*: add the "-w" option when asking for the diff.

.. _git-diff-algorithms:

Git Diff Algorithms
===================

Git offers four different algorithms in :code:`git diff`:

* Myers (default)
* Minimal (improved Myers)
* Patience (try to give contextual diff)
* Histogram (kind of enhanced patience)

`Differences between four diff algorithms`_

.. _Differences between four diff algorithms: https://git-scm.com/docs/git-diff#Documentation/git-diff.txt---diff-algorithmpatienceminimalhistogrammyers).

Based on the comparison between Myers and Histogram in a study by `Nugroho, et al (2019)`_, various :code:`diff` algorithms in the :code:`git diff` command produced unequal `diff` outputs.
From the result of patches analysis, they found that Histogram is better than Myers to show the changes of code that can be expected to recover the changing operations.
Thus, in this tool, we implement histogram :code:`diff` algorithm to consider differences in source code.

.. _Nugroho, et al (2019): https://doi.org/10.1007/s10664-019-09772-z