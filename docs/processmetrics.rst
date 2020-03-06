.. highlight:: python

==================
Process Metrics
==================

Process metrics capture aspects of the development process rather than aspects about the code itself.
From release 1.11 PyDriller can calculate ``code churn``, ``commits count``, ``contributors count``, ``contributors experience``, ``history complexity``, ``hunks count``, ``lines count`` and ``minor contributors``. Everything in just one line!

Below an example of how call the metrics.


Code Churn
===============

This metric measures the number of commits made to a file.
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
===============

This metric measures the number of commits made to a file.
For example::

    from pydriller.metrics.process.commits_count import CommitsCount
    metric = CommitsCount(path_to_repo='path/to/the/repo',
                          from_commit='from commit hash',
                          to_commit='to commit hash')
    files = metric.count()
    print('Files: {}'.format(files))

will print the number of commits for each modified file in the evolution period ``[from_commit, to_commit]``. 



Contributors Count
===============

This metric measures the number of developers that contributed to a file.
For example::

    from pydriller.metrics.process.contributors_count import ContributorsCount
    metric = ContributorsCount(path_to_repo='path/to/the/repo',
                               from_commit='from commit hash',
                               to_commit='to commit hash')
    files = metric.count()
    print('Files: {}'.format(files))

will print the number of developers that contributed to each of the modified file in the evolution period ``[from_commit, to_commit]``. 



Contributors Experience
===============

This metric measures the percetage of the lines authored by the highest contributor of a file.
For example::

    from pydriller.metrics.process.contributors_experience import ContributorsExperience
    metric = ContributorsExperience(path_to_repo='path/to/the/repo',
                          	    from_commit='from commit hash',
                                    to_commit='to commit hash')
    files = metric.count()
    print('Files: {}'.format(files))

will print the percentage of the lines authored by the highest contributor for each of the modified file in the evolution period ``[from_commit, to_commit]``. 



Hunks Count
===============

This metric measures the number of hunks made to a file.
As a hunk is a continuous block of changes in a ``diff``, this number assesses how fragmented the commit file is (i.e. lots of changes all over the file versus one big change).
For example::

    from pydriller.metrics.process.hunks_count import HunksCount
    metric = HunksCount(path_to_repo='path/to/the/repo',
                        from_commit='from commit hash',
                        to_commit='to commit hash')
    files = metric.count()
    print('Files: {}'.format(files))

will print the median number of hunks for each of the modified file in the evolution period ``[from_commit, to_commit]``. 



Lines Count
===============

This metric measures the number of added and removed lines in a file.
For example::

    from pydriller.metrics.process.lines_count import LinesCount
    metric = LinesCount(path_to_repo='path/to/the/repo',
                        from_commit='from commit hash',
                        to_commit='to commit hash')
    files = metric.count()
    print('Files: {}'.format(files))

will print a dictionary ``{'added': int, 'removed': int}`` of added and removed lines for each of the modified file in the evolution period ``[from_commit, to_commit]``. 


