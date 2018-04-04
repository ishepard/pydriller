.. _tutorial_toplevel:

.. highlight:: python

==================
Getting Started
==================

Using PyDriller is very simple. First, create a `RepositoryMining`: this class will receive in input the path to the repository and the visitor that will be called for every commit. For example::

    rp = RepositoryMining('path/to/the/repo', <visitor>)
    rp.mine()

Inside `RepositoryMining`, you will have to configure which projects to analyze, with how many threads, for which commits, etc. 

Let's start with something simple: we will print the name of the developers for each commit. For now, you should not care about all possible configurations. This does the magic::

    mv = MyVisitor()
    rp = RepositoryMining('test-repos/test1/', mv)
    rp.mine()

At this point, PyDriller will open the Git repository and will extract all information. Then, the framework will pass each commit to the visitor. Let's write our first visitor, it is fairly simple. All we will do is to implement CommitVisitor. And, inside of process(), we print the commit hash and the name of the developer::

    class MyVisitor(CommitVisitor):
        def process(self, repo: GitRepository, commit: Commit, writer: PersistenceMechanism):
            print("The hash: " + commit.hash)
            print("and the author: " + commit.author)

That's it! It's simple, isn't it?
