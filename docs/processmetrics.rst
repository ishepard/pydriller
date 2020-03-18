.. highlight:: python

==================
Process Metrics
==================

Process metrics capture aspects of the development process rather than aspects about the code itself.
From release 1.11 PyDriller can calculate ``change_set``, ``code churn``, ``commits count``, ``contributors count``, ``contributors experience``, ``history complexity``, ``hunks count``, ``lines count`` and ``minor contributors``. Everything in just one line!

The metrics can be run between two commits (setting up the parameters ``from_commit`` and ``to_commit``) or between two dates (setting up the parameters ``since`` and ``to``)

Below an example of how call the metrics.


Change Set
==========

This metric measures the of files committed together.

The class ``ChangeSet`` has two methods:

* ``max()`` to count the *maximum* number of files committed together;
* ``avg()`` to count the *average* number of files committed together. **Note:** The average value is rounded off to the nearest integer.

For example::

    from pydriller.metrics.process.change_set import ChangeSet
    metric = ChangeSet(path_to_repo='path/to/the/repo',
                       from_commit='from commit hash',
                       to_commit='to commit hash')
    
    maximum = metric.max()
    average = metric.avg()
    print('Maximum number of files committed together: {}'.format(maximum))
    print('Average number of files committed together: {}'.format(average))

will print the maximum and average number of files committed together in the evolution period ``[from_commit, to_commit]``. 

**Note:** differently from the other metrics below, the scope of this metrics is the evolution period rather than the single files.


It is possible to specify the dates as follows::

    from datetime import datetime
    from pydriller.metrics.process.change_set import ChangeSet
    metric = ChangeSet(path_to_repo='path/to/the/repo',
                       since=datetime(2019, 1, 1),
                       to=datetime(2019, 12, 31))
    
    maximum = metric.max()
    average = metric.avg()
    print('Maximum number of files committed together: {}'.format(maximum))
    print('Average number of files committed together: {}'.format(average))

The code above will print the maximum and average number of files committed together between the ``1st January 2019`` and ``31st December 2019``. 


Code Churn
==========

This metric measures the code churns of a file.
A code churn is the sum of (added lines - removed lines) across the analyzed commits.

The class ``CodeChurn`` has three methods:

* ``count()`` to count the *total* size of code churns of a file;
* ``max()`` to count the *maximum* size of a code churn of a file;
* ``avg()`` to count the *average* size of a code churn of a file. **Note:** The average value is rounded off to the nearest integer.

For example::

    from pydriller.metrics.process.code_churn import CodeChurn
    metric = CodeChurn(path_to_repo='path/to/the/repo',
                       from_commit='from commit hash',
                       to_commit='to commit hash')
    files_count = metric.count()
    files_max = metric.max()
    files_avg = metric.avg()
    print('Total code churn for each file: {}'.format(files_count))
    print('Maximum code churn for each file: {}'.format(files_max))
    print('Average code churn for each file: {}'.format(files_avg))

will print the total, maximum and average number of code churn for each modified file in the evolution period ``[from_commit, to_commit]``. 


Commits Count
=============

This metric measures the number of commits made to a file.

The class ``CommitCount`` has one method:

* ``count()`` to count the number of commits to a file.

For example::

    from pydriller.metrics.process.commits_count import CommitsCount
    metric = CommitsCount(path_to_repo='path/to/the/repo',
                          from_commit='from commit hash',
                          to_commit='to commit hash')
    files = metric.count()
    print('Files: {}'.format(files))

will print the number of commits for each modified file in the evolution period ``[from_commit, to_commit]``. 


Contributors Count
==================

This metric measures the number of developers that contributed to a file.

The class ``ContributorsCount`` has two methods:

* ``count()`` to count the number of contributors who modified a file;
* ``count_minor()`` to count the number of *minor* contributors who modified a file, i.e., those that contributed less than 5% to the file.

For example::

    from pydriller.metrics.process.contributors_count import ContributorsCount
    metric = ContributorsCount(path_to_repo='path/to/the/repo',
                               from_commit='from commit hash',
                               to_commit='to commit hash')
    count = metric.count()
    minor = metric.count_minor()
    print('Number of contributors per file: {}'.format(count))
    print('Number of "minor" contributors per file: {}'.format(minor))

will print the number of developers that contributed to each of the modified file in the evolution period ``[from_commit, to_commit]`` and the number of developers that contributed less than 5% to each of the modified file in the evolution period ``[from_commit, to_commit]``. 


Contributors Experience
========================

This metric measures the percetage of the lines authored by the highest contributor of a file.

The class ``ContriutorExperience`` has one method:

* ``count()`` to count the number of lines authored by the highest contributor of a file;

For example::

    from pydriller.metrics.process.contributors_experience import ContributorsExperience
    metric = ContributorsExperience(path_to_repo='path/to/the/repo',
                          	    from_commit='from commit hash',
                                    to_commit='to commit hash')
    files = metric.count()
    print('Files: {}'.format(files))

will print the percentage of the lines authored by the highest contributor for each of the modified file in the evolution period ``[from_commit, to_commit]``. 



Hunks Count
===========

This metric measures the number of hunks made to a file.
As a hunk is a continuous block of changes in a ``diff``, this number assesses how fragmented the commit file is (i.e. lots of changes all over the file versus one big change).

The class ``HunksCount`` has one method:

* ``count()`` to count the median number of hunks of a file.

For example::

    from pydriller.metrics.process.hunks_count import HunksCount
    metric = HunksCount(path_to_repo='path/to/the/repo',
                        from_commit='from commit hash',
                        to_commit='to commit hash')
    files = metric.count()
    print('Files: {}'.format(files))

will print the median number of hunks for each of the modified file in the evolution period ``[from_commit, to_commit]``. 


Lines Count
===========

This metric measures the number of added and removed lines in a file.
The class ``LinesCount`` has seven methods:

* ``count()`` to count the total number of added and removed lines for each modified file;
* ``count_added()``, ``max_added()`` and ``avg_added()`` to count the total, maximum and average number of added lines for each modified file;
* ``count_removed()``, ``max_removed()`` and ``avg_removed()`` to count the total, maximum and average number of removed lines for each modified file.

**Note:** The average values are rounded off to the nearest integer.

For example::

    from pydriller.metrics.process.lines_count import LinesCount
    metric = LinesCount(path_to_repo='path/to/the/repo',
                        from_commit='from commit hash',
                        to_commit='to commit hash')
    
    added_count = metric.count_added()
    added_max = metric.max_added()
    added_avg = metric.avg_added()
    print('Total lines added per file: {}'.format(added_count))
    print('Maximum lines added per file: {}'.format(added_max))
    print('Average lines added per file: {}'.format(added_avg))

will print the total, maximum and average number of lines added for each modified file in the evolution period ``[from_commit, to_commit]``. 

While::

    from pydriller.metrics.process.lines_count import LinesCount
    metric = LinesCount(path_to_repo='path/to/the/repo',
                        from_commit='from commit hash',
                        to_commit='to commit hash')
    
    removed_count = metric.count_removed()
    removed_max = metric.max_removed()
    removed_avg = metric.avg_removed()
    print('Total lines removed per file: {}'.format(removed_count))
    print('Maximum lines removed per file: {}'.format(removed_max))
    print('Average lines removed per file: {}'.format(removed_avg))

will print the total, maximum and average number of lines removed for each modified file in the evolution period ``[from_commit, to_commit]``. 
