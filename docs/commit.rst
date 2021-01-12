.. _commit_toplevel:

=============
Commit 
=============

A Commit object has all the information of a Git commit, and much more. More specifically:

* **hash** *(str)*: hash of the commit
* **msg** *(str)*: commit message
* **author** *(Developer)*: commit author (name, email)
* **committer** *(Developer)*: commit committer (name, email) 
* **author_date** *(datetime)*: authored date
* **author_timezone** *(int)*: author timezone (expressed in seconds from epoch)
* **committer_date** *(datetime)*: commit date
* **committer_timezone** *(int)*: commit timezone (expressed in seconds from epoch)
* **branches** *(List[str])*: List of branches that contain this commit
* **in_main_branch** *(Bool)*: True if the commit is in the main branch
* **merge** *(Bool)*: True if the commit is a merge commit
* **modifications** *(List[Modifications])*: list of modified files in the commit (see :ref:`modifications_toplevel`)
* **parents** *(List[str])*: list of the commit parents
* **project_name** *(str)*: project name 
* **project_path** *(str)*: project path 
* **deletions** *(int)*: number of deleted lines in the commit (as shown from –shortstat).
* **insertions** *(int)*: number of added lines in the commit (as shown from –shortstat).
* **lines** *(int)*: total number of added + deleted lines in the commit (as shown from –shortstat).
* **files** *(int)*: number of files changed in the commit (as shown from –shortstat).
* **dmm_unit_size** *(float)*: DMM metric value for the unit size property.
* **dmm_unit_complexity** *(float)*: DMM metric value for the unit complexity property.
* **dmm_unit_interfacing** *(float)*: DMM metric value for the unit interfacing property.


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
