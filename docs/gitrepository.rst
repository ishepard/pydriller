.. _gitrepository_toplevel:

==============
Git Repository
==============

GitRepository is a wrapper for the most common utilities of Git. It receives in input
the path to repository, and it takes care of the rest. 
For example, with GitRepository you can checkout a specific commit::

    gr = GitRepository('test-repos/git-1/')
    gr.checkout('a7053a4dcd627f5f4f213dc9aa002eb1caf926f8')

However, **be careful!** Git checkout changes the state of the repository on the hard
disk, hence you should not use this command if other processes (maybe threads? or multiple 
repository mining?) read from the same repository.

GitRepository also contains a function to parse the a `diff`, very useful to obtain the list
of lines added or deleted for future analysis. For example, if we run this::

    diff = '@@ -2,6 +2,7 @@ aa'+\
        ' bb'+\
        '-cc'+\
        ' log.info(\"aa\")'+\
        '+log.debug(\"b\")'+\
        ' dd'+\
        ' ee'+\
        ' ff'
    gr = GitRepository('test-repos/test1')
    parsed_lines = gr.parse_diff(diff)

    added = parsed_lines['added']
    deleted = parsed_lines['deleted']

    print('Added: {}'.format(added))      # result: Added: [(4, 'log.debug("b")')]
    print('Deleted: {}'.format(deleted))  # result: Deleted: [(3, 'cc')]

the result is::

    Added: [(4, 'log.debug("b")')]
    Deleted: [(3, 'cc')]

Another very useful API (especially for researchers ;) ) is the one that, given a commit, allows you to retrieve
all the commits that last "touched" the modified lines of the file (if you pass a bug fixing commit, it will retrieve the bug inducing). Let's see an example::

    # commit abc modified line 1 of file A
    # commit def modified line 2 of file A
    # commit ghi modified line 3 of file A
    # commit lmn deleted lines 1 and 2 of file A
    
    gr = GitRepository('test-repos/test5')
    
    commit = gr.getcommit('lmn')
    buggy_commits = gr.get_commits_last_modified_lines(commit)
    print(buggy_commits)      # result: (abc, def)

Since in commit **lmn** 2 lines were deleted (line 1 and 2), PyDriller can retrieve the commits in which those lines
were last modified (in our example, commit **abc** and **def**).

Isn't it cool? :) 

Checkout the API reference of this class for the complete list of the available functions.

