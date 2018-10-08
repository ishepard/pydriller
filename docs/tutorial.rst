.. _tutorial_toplevel:

.. highlight:: python

==================
Getting Started
==================

Using PyDriller is very simple. You only need to create `RepositoryMining`: this class will receive in input the path to the repository and will return a generator that iterates over the commits. For example::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        print('Hash {}, author {}'.format(commit.hash, commit.author.name))

will print the name of the developers for each commit. 

Inside `RepositoryMining`, you will have to configure which projects to analyze, for which commits, for which dates etc. For all the possible configurations, have a look at :ref:`configuration_toplevel`.

Let's make another example: print all the modified files for every commit. This does the magic::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        for modification in commit.modifications:
            print('Author {} modified {} in commit {}'.format(commit.author.name, modification.filename, commit.hash))

That's it!

Behind the scenes, PyDriller opens the Git repository and extracts all the necessary information. Then, the framework returns a generator that can iterate over the commits. 

Ok, let's try a more difficult problem: let's count how many commits contain the word "bug" in the message. We can do it like this::

    count = 0
    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        if 'bug' in commit.msg:
            count += 1

Furthermore, PyDriller can calculate structural metrics of every file changed in a commit. To calculate these metrics, Pydriller relies on `Lizard <https://github.com/terryyin/lizard>`_, a powerful tool that can analyze source code of many different programming languages, both at class and method level! ::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        for mod in commit.modifications:
            print('{} has complexity of {}, and it contains {} methods'.format(
                  mod.filename, mod.complexity, len(mod.methods))