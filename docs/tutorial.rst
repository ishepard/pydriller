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

We can also pass a list of repositories (both local and remote), and PyDriller will analyze sequentially. In case of a remote repository, PyDriller will clone it in a temporary folder, and delete it afterwards. For example::

    urls = ["repos/repo1", "repos/repo2", "https://github.com/ishepard/pydriller.git", "repos/repo3", "https://github.com/apache/hadoop.git"]
    for commit in RepositoryMining(path_to_repo=urls).traverse_commits():
        print("Project {}, commit {}, date {}".format(
               commit.project_path, commit.hash, commit.author_date))


Let's make another example: print all the modified files for every commit. This does the magic::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        for modification in commit.modifications:
            print('Author {} modified {} in commit {}'.format(commit.author.name, modification.filename, commit.hash))

That's it!

Behind the scenes, PyDriller opens the Git repository and extracts all the necessary information. Then, the framework returns a generator that can iterate over the commits. 

Furthermore, PyDriller can calculate structural metrics of every file changed in a commit. To calculate these metrics, Pydriller relies on `Lizard <https://github.com/terryyin/lizard>`_, a powerful tool that can analyze source code of many different programming languages, both at class and method level! ::

    for commit in RepositoryMining('path/to/the/repo').traverse_commits():
        for mod in commit.modifications:
            print('{} has complexity of {}, and it contains {} methods'.format(
                  mod.filename, mod.complexity, len(mod.methods))