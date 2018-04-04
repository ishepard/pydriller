[![Build Status](https://travis-ci.com/ishepard/pydriller.svg?token=J3YWhdMEr4RvUk6qZbMK&branch=master)](https://travis-ci.com/ishepard/pydriller)
[![BCH compliance](https://bettercodehub.com/edge/badge/ishepard/pydriller?branch=master&token=fdd54de940e65d248cd892ac8791a1445f38c88f)](https://bettercodehub.com/)


# PyDriller

PyDriller is a Python framework that helps developers on mining software repositories. Born as a fork of [RepoDriller](https://github.com/mauricioaniche/repodriller), with PyDriller you can easily extract information from any Git repository, such as commits, developers, modifications, diffs, and source codes, and quickly export CSV files.

<!--Take a look at our [manual folder](https://www.github.com/mauricioaniche/repodriller/tree/master/manual) and [our many examples](https://github.com/mauricioaniche/repodriller-tutorial).-->


# REQUIREMENTS
Very few! Just:

- Python3
- Git

The list of dependencies are listed in ./requirements.txt, however the installer takes care of installing them for you.

# INSTALL

Installing PyDriller is easily done using pip. Assuming it is installed, just run the following from the command-line:

```
pip install pydriller
```
This will also install the necessary dependencies.

# SOURCE CODE

If you like to clone from source, you can do it like so:

## OPTIONAL

It is suggested to make use of `virtualenv`:

```
> virtualenv -p python3 venv
> source venv/bin/activate
```

## INSTALL FROM SOURCE
Clone the repo:

```
> git clone https://github.com/ishepard/pydriller.git
```

install the requirements:

```
> cd pydriller
> pip install -r requirements
```
and run the tests using pytest:

```
> pytest
```


# GETTING STARTED
Using PyDriller is very simple. First, create a `RepositoryMining`: this class will receive in input the path to the repository and the visitor that will be called for every commit. For example:

```
rp = RepositoryMining('path/to/the/repo', <visitor>)
rp.mine()
```
Inside `RepositoryMining`, you will have to configure which projects to analyze, with how many threads, for which commits, etc. 

Let's start with something simple: we will print the name of the developers for each commit. For now, you should not care about all possible configurations. This does the magic:

```
mv = MyVisitor()
rp = RepositoryMining('test-repos/test1/', mv)
rp.mine()
```

At this point, PyDriller will open the Git repository and will extract all information. Then, the framework will pass each commit to the visitor. Let's write our first visitor, it is fairly simple. All we will do is to implement CommitVisitor. And, inside of process(), we print the commit hash and the name of the developer:

```
class MyVisitor(CommitVisitor):
    def process(self, repo: GitRepository, commit: Commit, writer: PersistenceMechanism):
        print("The hash: " + commit.hash)
        print("and the author: " + commit.author)
```

That's it! It's simple, isn't it?


## Selecting the Commit Range
By default, PyDriller executes the visitor for all the commits in the repository. However, filters can be applied to `RepositoryMining` to visit _only specific_ commits. 

- *single: str*: single hash of the commit. The visitor will be called only on this commit

_FROM_

- *since: datetime*: only commits after this date will be analyzed
- *from_commit: str*: only commits after this commit hash will be analyzed
- *from_tag: str*: only commits after this commit tag will be analyzed

_TO_

- *to: datetime*: only commits up to this date will be analyzed
- *to_commit: str*: only commits up to this commit hash will be analyzed
- *to_tag: str*: only commits up to this commit tag will be analyzed

Examples:

```
mv = VisitorTest()

# Analyze single commit
RepositoryMining('test-repos/git-4/', mv, single='6411e3096dd2070438a17b225f44475136e54e3a').mine()

# Since 8/10/2016
RepositoryMining('test-repos/git-4/', mv, since=datetime(2016, 10, 8, 17, 0, 0).mine()

# Between 2 dates
dt1 = datetime(2016, 10, 8, 17, 0, 0)
dt2 = datetime(2016, 10, 8, 17, 59, 0)
RepositoryMining('test-repos/git-4/', mv, since=dt1, to=dt2).mine()

# Between tags
from_tag = 'tag1'
to_tag = 'tag2'
RepositoryMining('test-repos/git-4/', mv, from_tag=from_tag, to_tag=to_tag).mine()

# Up to a date
dt1 = datetime(2016, 10, 8, 17, 0, 0, tzinfo=to_zone)
RepositoryMining('test-repos/git-4/', mv, to=dt1).mine()

# ERROR!! THIS IS NOT POSSIBLE
RepositoryMining('test-repos/test1/', mv, from_tag=from_tag, from_commit=from_commit)
```

**IMPORTANT**: it is **not** possible to configure more than one filter of the same category (for example, more than one *from*). It is also **not** possible to have the *single* filter together with other filters!

## Filtering commits
PyDriller comes with a set of common commit filters that you can apply:

- *only\_in\_branches: List[str]*: only visits commits that belong to certain branches.
- *only\_in\_main\_branch: bool*: only visits commits that belong to the main branch of the repository.
- *only\_no\_merge: bool*: only visits commits that are not merge commits.
- *only\_modifications\_with\_file\_types: List[str]*: only visits commits in which at least one modification was done in that file type, e.g., if you pass ".java", then, the it will visit only commits in which at least one Java file was modified; clearly, it will skip other commits.

Examples:

```
mv = VisitorTest()

# Only commits in main branch
RepositoryMining('test-repos/git-5/', mv, only_in_main_branch=True).mine()

# Only commits in main branch and no merges
RepositoryMining('test-repos/git-5/', mv, only_in_main_branch=True, only_no_merge=True).mine()

# Only commits that modified a java file
RepositoryMining('test-repos/git-5/', mv, only_modifications_with_file_types=['.java']).mine()
```

## Commit
A Commit contains a hash, a committer (name and email), an author (name, and email) a message, the date, a list of its parent hashes (if it's a merge commit, the commit has two parents), and the list of modification.

For example:

```
class MyVisitor(CommitVisitor):
    def process(self, repo: GitRepository, commit: Commit, writer: PersistenceMechanism):
        print(
            'Hash: {}\n'.format(commit.hash),
            'Author: {}'.format(commit.author.name),
            'Committer: {}'.format(commit.committer.name),
            'Author date: {}'.format(commit.author_date.strftime("%Y-%m-%d %H:%M:%S")),
            'Message: {}'.format(commit.msg),
            'Merge: {}'.format(commit.merge),
            'In main branch: {}'.format(commit.in_main_branch)
        )
```

## Modifications
You can get the list of modified files, as well as their diffs and current source code. To that, all you have to do is to get the list of _Modification_s that exists inside Commit. A modification object has the following fields:

- *old_path*: old path of the file (can be _None_ if the file is added)
- *new_path*: new path of the file (can be null if the file is deleted)
- *change_type*: type of the change 
- *diff*: diff of the change
- *source_code*: source code of the file (can be null if the file is deleted)
- *added*: number of lines added
- *removed*: number of lines removed
- *filename*: filename

For example:

```
class MyVisitor(CommitVisitor):
    def process(self, repo: GitRepository, commit: Commit, writer: PersistenceMechanism):
        for m in commit.modifications:
            print(
                "Author {}".format(commit.author.name),
                " modified {}".format(m.filename),
                " with a change type of {}".format(m.change_type.name)
            )
```


## How do I cite PyDriller?

For now, cite the repository.


# License

This software is licensed under the Apache 2.0 License.
