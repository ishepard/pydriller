.. _commit_toplevel:

=============
Commit Object
=============

A Commit object has all the information of a Git commit, and much more. More specifically:

* **hash** *(str)*: hash of the commit
* **msg** *(str)*: commit message
* **author** *(Developer)*: commit author (name, email)
* **author_date** *(datetime)*: authored date
* **author_timezone** *(int)*: author timezone (expressed in seconds from epoch)
* **committer** *(Developer)*: commit committer (name, email) 
* **committer_date** *(datetime)*: commit date
* **committer_timezone** *(int)*: commit timezone (expressed in seconds from epoch)
* **branches** *(List[str])*: List of branches that contain this commit
* **in_main_branch** *(Bool)*: True if the commit is in the main branch
* **merge** *(Bool)*: True if the commit is a merge commit
* **modifications** *(List[Modifications])*: list of modified files in the commit (see :ref:`modifications_toplevel`)
* **parents** *(Set[str])*: list of the commit parents
* **project_name** *(str)*: project name 
* **project_path** *(str)*: project path 


Example::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        print(
            'The commit {} has been modified by {}, '
            'committed by {} in date {}'.format(
                commit.hash,
                commit.author.name,
                commit.committer.name,
                commit.committer_date
            )
        )
