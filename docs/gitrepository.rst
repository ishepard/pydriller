.. _gitrepository_toplevel:

==============
GitRepository
==============

GitRepository is a wrapper for the most common utilities of Git, such as checkout and reset.
For example, to checkout a specific commit or branch::

    gr = GitRepository('test-repos/git-1/')
    gr.checkout('a7053a4dcd627f5f4f213dc9aa002eb1caf926f8')

However, **be careful!** Git checkout changes the state of the repository on the hard
disk, hence you should not use this command if other processes (maybe threads? or multiple 
repository mining?) read from the same repository.

Moreover, GitRepository can be used to obtain different information from the repository::

    gr = GitRepository('test-repos/test1')
    gr.get_list_commits()                  # get the list of all commits
    gr.get_commit('cc5b002')               # get the specific commit
    gr.files()                             # get the list of files present in the repo at the current commit
    gr.total_commits()                     # get total number of commits
    gr.get_commit_from_tag('v1.15')        # get the commit with tag v1.15

Another very useful API (especially for researchers ;) ) is the one that, given a commit, allows you to retrieve
all the commits that last "touched" the modified lines of the file (if you pass a bug fixing commit, it will retrieve the bug inducing). 

PS: Since PyDriller 1.9, this function can be customized to use "git hyper-blame" (check `this <https://commondatastorage.googleapis.com/chrome-infra-docs/flat/depot_tools/docs/html/depot_tools_tutorial.html#_setting_up>`_ for more info).
Git hyper blame can be instructed to skip specific commits (like commits that refactor the code).

Let's see an example::

    # commit abc modified line 1 of file A
    # commit def modified line 2 of file A
    # commit ghi modified line 3 of file A
    # commit lmn deleted lines 1 and 2 of file A
    
    gr = GitRepository('test-repos/test5')
    
    commit = gr.get_commit('lmn')
    buggy_commits = gr.get_commits_last_modified_lines(commit)
    print(buggy_commits)      # result: (abc, def)

Since in commit **lmn** 2 lines were deleted (line 1 and 2), PyDriller can retrieve the commits in which those lines
were last modified (in our example, commit **abc** and **def**).

Checkout the :ref:`api_reference_toplevel` of this class for the complete list of the available functions.
