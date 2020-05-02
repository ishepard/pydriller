.. _deltamaintainability:

=====================
Delta Maintainability
=====================

Background
==========

To assess the maintainability implications of commits, PyDriller offers an implementation of the *Open Source Delta Maintainability Model* (OS-DMM). The underlying Delta Maintainability Model was originally described in a paper that appeared at TechDebt 2019 [DiBiase2019]_.
A commercially available implementation supporting over 100 different languages with fine-grained analysis is offered by the `Software Improvement Group <https://www.softwareimprovementgroup.com/>`_ (SIG).

The Open Source implementation included in PyDriller offers a partial implementation suitable for research experiments and measurements for systems written in common programming languages already supported by PyDriller. While the git-functionality of PyDriller is language agnostic, the *metrics* (such as method size and cyclomatic complexity) it supports require language-specific implementations -- for  which PyDriller relies on `Lizard <https://github.com/terryyin/lizard>`_.

The OS-DMM implementation extends the PyDriller metrics with three commit-level metrics related to risk in size, complexity, and interfacing.

Definition
==========

In one sentence, the delta-maintainability metric is the proportion of *low-risk change* in a commit. The resulting value ranges from 0.0 (all changes are risky) to 1.0 (all changes are low risk). It rewards making methods better, and penalizes making things worse.

The starting point for the DMM is a *risk profile* [Heitlager2007]_. Traditionally, risk profiles categorize methods (or, more generally, also referred to as *units*) into four bins: low, medium, high, and very high risk methods. The risk profile of a class then is a 4-tuple (*l, m, h, v*) representing the amount of code (number of lines) in each of the four  categories.

For simplicity, in the context of the DMM, only two bins are used: low risk, and non-low (medium, high, or very high) risk. To transfer risk profiles from file (or system) level to commit level, we consider *delta risk profiles*. These are pairs (*dl, dh*), with *dl* being the increase (or decrease) of low risk code, and *dh* the increase (or decrease) in high risk code.

The delta risk profile can then be used to determine good and bad change:

- Increases in low risk code are good, but increases in high risk code are bad.
- Decreases in high risk code are good, and decreases in low risk code are good only if no high risk code is added instead, and bad otherwise.

The dmm value is then computed as: *good change / (good change + bad change)*.

.. _Properties:

Properties
==========

The DMM can be used on arbitrary properties that can be determined at method (unit) level. The PyDriller OS-DMM implementation supports three properties:

- Unit **size**: Method length in lines of code; low risk threshold 15 lines.
- Unit **complexity**: Method cyclomatic complexity; low risk threshold 5.
- Unit **interfacing**: Method number of parameters: low risk threshold 2.

The original DMM paper also used coupling and cloned code as properties, but these are not easily computed per commit with the Lizard infrastructure. The thresholds are language-independent by design, and have been determined empirically following the procedure described in [Alves2010]_, using industrial benchmark data collected by SIG [SIG2019]_.

Example usage
=============

Collecting DMM values from a git repository is  straightforward::

	from pydriller import RepositoryMining

	rm = RepositoryMining("https://github.com/avandeursen/dmm-test-repo")
	for commit in rm.traverse_commits():
		print("| {} | {} | {} | {} |".format(
			commit.msg,
			commit.dmm_unit_size,
			commit.dmm_unit_complexity,
			commit.dmm_unit_interfacing
			))

The resulting ``dmm`` values are proportions with values between 0.0 and 1.0.
Files that are changed in a commit, but which are written in languages not supported  by PyDriller (Lizard) are ignored -- these are often configuration (``.xml``, ``.yaml``) or documentation (``.txt``, ``.md``) files.
If none of the files changed in a commit are in languages supported by Pydriller, the ``dmm`` value is ``None``.


Under the hood
==============

The main public API consists of the three ``dmm_unit_size``, ``dmm_unit_complexity``, and ``dmm_unit_interfacing`` properties on the ``Commit`` class, as illustrated above.
Under the hood, the DMM implementation can be easily configured or accessed:

- The thresholds are set as separate constants in the ``Method`` class;
- The main methods implementing the DMM  are parameterized with an enum characterizing the DMM property of interest.
- There are separate (protected) methods to compute risk profiles and delta-risk profiles at ``Commit`` and ``Modification`` level, which can be used to collect more detailed information for selected (e.g., lowly rated) commits.


Relation to SIG DMM
===================

PyDriller's OS-DMM and SIG's DMM differ in the following ways:

- OS-DMM offers only support for the approximately 15 languages supported by `Lizard <https://github.com/terryyin/lizard>`_.
- OS-DMM relies on Lizard for the identification of *methods* (units) in source files. While for simple cases SIG and Lizard tooling will agree, this may not be the case for more intricate cases involving e.g., lambdas, inner classes, nested functions, etc.
- OS-DMM relies on Lizard for simple line counting, which also counts white space. SIG's DMM on the other hand ignores blank lines.
- OS-DMM uses the thresholds as empirically determined by SIG, based on SIG's measurement methodology [Alves2010]_. OS-DMM's Lizard-based metric values may be different, and hence may classify methods in different risk bins for methods close to the thresholds.

Consequently, individual DMM values are likely to differ a few percentage points between the SIG DMM and OS-DMM implementations. However, in terms of trends and statistical analysis, the outcomes will likely be very similar.
Therefore:

- For research purposes, we recommend the fully open PyDriller implementation ensuring reproducible results.
- For commercial purposes including day to day monitoring of maintainability at commit, code, file, component, project, and portfolio level, we recommend the more robust SIG implementation.

References
==========

.. [DiBiase2019] Marco di Biase, Ayushi Rastogi, Magiel Bruntink, and Arie van Deursen. **The Delta Maintainability Model: measuring maintainability of fine-grained code changes**. IEEE/ACM International Conference on Technical Debt (TechDebt) at ICSE 2019, pp 113-122 (`preprint <https://pure.tudelft.nl/portal/en/publications/the-delta-maintainability-model-measuring-maintainability-of-finegrained-code-changes(6ff67dee-2781-47d7-916f-bd36c5b61beb).html>`_, `doi <https://doi.org/10.1109/TechDebt.2019.00030>`_).

.. [Heitlager2007] Ilja Heitlager, Tobias Kuipers, and Joost Visser. **A Practical Model for Measuring Maintainability**. 6th International Conference on the Quality of Information and Communications Technology, QUATIC 2007, IEEE, pp 30-39 (`preprint <http://wiki.di.uminho.pt/twiki/pub/Personal/Joost/PublicationList/HeitlagerKuipersVisser-Quatic2007.pdf>`_, `doi <https://doi.org/10.1109/QUATIC.2007.8>`_)

.. [Alves2010] Tiaga Alves, Christiaan Ypma, and Joost Visser. **Deriving metric thresholds from benchmark data**. IEEE International Conference on Software Maintenance (ICSM), pages 1–10. IEEE, 2010 (`preprint <http://wiki.di.uminho.pt/twiki/pub/Personal/Tiago/Publications/icsm10rt-alves.pdf>`_, `doi <https://doi.org/10.1109/ICSM.2010.5609747>`_).

.. [SIG2019] Reinier Vis, Dennis Bijslma, and Haiyun Xu. SIG/TÜViT Evaluation Criteria Trusted Product  Maintainability:  Guidance for producers. Version 11.0. Software Improvement Group, 2019 (`online <https://www.softwareimprovementgroup.com/wp-content/uploads/2019/11/20190919-SIG-TUViT-Evaluation-Criteria-Trusted-Product-Maintainability-Guidance-for-producers.pdf>`_).