.. _configuration_toplevel:

=============
Configuration
=============

One of the main advantage of using PyDriller to mine software repositories, is that is highly configurable. Let's start with selecting which commit to analyze.

Selecting projects to analyze
=============================
The only required parameter of `RepositoryMining` is **path_to_repo**, which specifies the repo(s) to analyze. It must be of type `str` or `List[str]`, meaning analyze only one repository or more than one.

Furthermore, PyDriller supports both local and remote repositories: if you pass an URL, PyDriller will automatically create a temporary folder, clone the repository, run the study, and finally delete the temporary folder. 

For example, the following are all possible inputs for `RepositoryMining`::
    
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

By default, PyDriller analyzes all the commits in the repository. However, filters can be applied to `RepositoryMining` to visit *only specific* commits. 

* **single** *(str)*: single hash of the commit. The visitor will be called only on this commit

*FROM*:

* **since** *(datetime)*: only commits after this date will be analyzed
* **from_commit** *(str)*: only commits after this commit hash will be analyzed
* **from_tag** *(str)*: only commits after this commit tag will be analyzed

*TO*:

* **to** *(datetime)*: only commits up to this date will be analyzed
* **to_commit** *(str)*: only commits up to this commit hash will be analyzed
* **to_tag** *(str)*: only commits up to this commit tag will be analyzed

*ORDER*:

* **reversed\_order** *(bool)*: by default PyDriller returns the commits in chronological order (from the oldest to the newest, the contrary of `git log`). If you need viceversa instead, put this field to **True**.

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

* **only\_in\_branch** *(str)*: only analyses commits that belong to this branch.
* **only\_no\_merge** *(bool)*: only analyses commits that are not merge commits.
* **only\_authors** *(List[str])*: only analyses commits that are made by these authors. The check is made on the username, NOT the email.
* **only\_commits** *(List[str])*: only these commits will be analyzed.
* **filepath** *(str)*: only commits that modified this file will be analyzed.
* **only\_modifications\_with\_file\_types** *(List[str])*: only analyses commits in which at least one modification was done in that file type, e.g., if you pass ".java", then, the it will visit only commits in which at least one Java file was modified; clearly, it will skip other commits.

Examples::

    # Only commits in branch1
    RepositoryMining('path/to/the/repo', only_in_branch='branch1').traverse_commits()

    # Only commits in branch1 and no merges
    RepositoryMining('path/to/the/repo', only_in_branch='branch1', only_no_merge=True).traverse_commits()

    # Only commits of author "ishepard" (yeah, that's me)
    RepositoryMining('path/to/the/repo', only_authors=['ishepard']).traverse_commits()

    # Only these 3 commits
    RepositoryMining('path/to/the/repo', only_commits=['hash1', 'hash2', 'hash3']).traverse_commits()

    # Only commit that modified "Matricula.javax" 
    RepositoryMining('path/to/the/repo', filepath='Matricula.javax').traverse_commits()

    # Only commits that modified a java file
    RepositoryMining('path/to/the/repo', only_modifications_with_file_types=['.java']).traverse_commits()



