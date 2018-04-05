.. _tutorial_toplevel:

.. highlight:: python

==================
Getting Started
==================

Using PyDriller is very simple. You only need to create `RepositoryMining`: this class will receive in input the path to the repository and return a generator that iterates over the commits. For example::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        print('Hash {}, author {}'.format(commit.hash, commit.author.name))

will print the name of the developers for each commit. It's simple, isn't it? 

Inside `RepositoryMining`, you will have to configure which projects to analyze, for which commits, for which dates etc. For all the possible configurations, have a look at :ref:`configuration_toplevel`.

Let's make another example: print all the modified files for every commit. This does the magic::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        for modification in commit.modifications:
            if modification.change_type == ModificationType.MODIFY:
                print('Author {} modified {} in commit {}'.format(commit.author.name, modification.filename, commit.hash))

That's it! It's simple, isn't it?

Behind the scenes, PyDriller opens the Git repository and extracts all the necessary information. Then, the framework returns a generator that can iterate over the commits. 
