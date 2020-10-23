import logging
from _datetime import datetime
from typing import List, Set, Tuple, Optional

from git import Diff, Git, Commit as GitCommit, NULL_TREE

from pydriller.domain.developer import Developer
from pydriller.domain.commit import Commit, Modification, ModificationType, DMMProperty

logger = logging.getLogger(__name__)


class CommitGP(Commit):
    """
    Class representing a Commit. Contains all the important information such
    as hash, author, dates, and modified files.
    """

    def __init__(self, commit: GitCommit, conf) -> None:
        """
        Create a commit object.

        :param commit: GitGP Commit object
        :param conf: Configuration class
        """

        super().__init__(commit, conf)

    @property
    def hash(self) -> str:
        """
        Return the SHA of the commit.

        :return: str hash
        """
        return self._c_object.hexsha

    @property
    def author(self) -> Developer:
        """
        Return the author of the commit as a Developer object.

        :return: author
        """
        return Developer(self._c_object.author.name,
                         self._c_object.author.email)

    @property
    def committer(self) -> Developer:
        """
        Return the committer of the commit as a Developer object.

        :return: committer
        """
        return Developer(self._c_object.committer.name,
                         self._c_object.committer.email)

    @property
    def author_date(self) -> datetime:
        """
        Return the authored datetime.

        :return: datetime author_datetime
        """
        return self._c_object.authored_datetime

    @property
    def committer_date(self) -> datetime:
        """
        Return the committed datetime.

        :return: datetime committer_datetime
        """
        return self._c_object.committed_datetime

    @property
    def author_timezone(self) -> int:
        """
        Author timezone expressed in seconds from epoch.

        :return: int timezone
        """
        return self._c_object.author_tz_offset

    @property
    def committer_timezone(self) -> int:
        """
        Author timezone expressed in seconds from epoch.

        :return: int timezone
        """
        return self._c_object.committer_tz_offset

    @property
    def msg(self) -> str:
        """
        Return commit message.

        :return: str commit_message
        """
        return self._c_object.message.strip()

    @property
    def parents(self) -> List[str]:
        """
        Return the list of parents SHAs.

        :return: List[str] parents
        """
        parents = []
        for p in self._c_object.parents:
            parents.append(p.hexsha)
        return parents

    @property
    def merge(self) -> bool:
        """
        Return True if the commit is a merge, False otherwise.

        :return: bool merge
        """
        return len(self._c_object.parents) > 1

    @property
    def modifications(self) -> List[Modification]:
        """
        Return a list of modified files. The list is empty if the commit is
        a merge commit. For more info on this, see
        https://haacked.com/archive/2014/02/21/reviewing-merge-commits/ or
        https://github.com/ishepard/pydriller/issues/89#issuecomment-590243707

        :return: List[Modification] modifications
        """
        if self._modifications is None:
            self._modifications = self._get_modifications()

        assert self._modifications is not None
        return self._modifications

    def _get_modifications(self):
        options = {}
        if self._conf.get('histogram'):
            options['histogram'] = True

        if self._conf.get('skip_whitespaces'):
            options['w'] = True

        if len(self.parents) == 1:
            # the commit has a parent
            diff_index = self._c_object.parents[0].diff(self._c_object,
                                                        create_patch=True,
                                                        **options)
        elif len(self.parents) > 1:
            # if it's a merge commit, the modified files of the commit are the
            # conflicts. This because if the file is not in conflict,
            # pydriller will visit the modification in one of the previous
            # commits. However, parsing the output of a combined diff (that
            # returns the list of conflicts) is challenging: so, right now,
            # I will return an empty array, in the meanwhile I will try to
            # find a way to parse the output.
            # c_git = GitGP(str(self.project_path))
            # d = c_git.diff_tree("--cc", commit.hexsha, '-r', '--abbrev=40',
            #                     '--full-index', '-M', '-p', '--no-color')
            diff_index = []
        else:
            # this is the first commit of the repo. Comparing it with git
            # NULL TREE
            diff_index = self._c_object.diff(NULL_TREE,
                                             create_patch=True,
                                             **options)

        return self._parse_diff(diff_index)

    def _parse_diff(self, diff_index) -> List[Modification]:
        modifications_list = []
        for diff in diff_index:
            old_path = diff.a_path
            new_path = diff.b_path
            change_type = self._from_change_to_modification_type(diff)

            diff_and_sc = {
                'diff': self._get_decoded_str(diff.diff),
                'source_code_before': self._get_decoded_sc_str(
                    diff.a_blob),
                'source_code': self._get_decoded_sc_str(
                    diff.b_blob)
            }

            modifications_list.append(Modification(old_path, new_path,
                                                   change_type, diff_and_sc))

        return modifications_list

    def _get_decoded_str(self, diff):
        try:
            return diff.decode('utf-8', 'ignore')
        except (UnicodeDecodeError, AttributeError, ValueError):
            logger.debug('Could not load the diff of a '
                         'file in commit %s', self._c_object.hexsha)
            return None

    def _get_decoded_sc_str(self, diff):
        try:
            return diff.data_stream.read().decode('utf-8', 'ignore')
        except (UnicodeDecodeError, AttributeError, ValueError):
            logger.debug('Could not load source code of a '
                         'file in commit %s', self._c_object.hexsha)
            return None

    @property
    def in_main_branch(self) -> bool:
        """
        Return True if the commit is in the main branch, False otherwise.

        :return: bool in_main_branch
        """
        return self._conf.get('main_branch') in self.branches

    @property
    def branches(self) -> Set[str]:
        """
        Return the set of branches that contain the commit.

        :return: set(str) branches
        """
        if self._branches is None:
            self._branches = self._get_branches()

        assert self._branches is not None
        return self._branches

    def _get_branches(self):
        c_git = Git(str(self._conf.get('path_to_repo')))
        branches = set()
        for branch in set(c_git.branch('--contains', self.hash).split('\n')):
            branches.add(branch.strip().replace('* ', ''))
        return branches

    @property
    def dmm_unit_size(self) -> Optional[float]:
        """
        Return the Delta Maintainability Model (DMM) metric value for the unit size property.

        It represents the proportion (between 0.0 and 1.0) of maintainability improving
        change, when considering the lengths of the modified methods.

        It rewards (value close to 1.0) modifications to low-risk (small) methods,
        or spliting risky (large) ones.
        It penalizes (value close to 0.0) working on methods that remain large
        or get larger.

        :return: The DMM value (between 0.0 and 1.0) for method size in this commit,
                 or None if none of the programming languages in the commit are supported.
        """
        return self._delta_maintainability(DMMProperty.UNIT_SIZE)

    @property
    def dmm_unit_complexity(self) -> Optional[float]:
        """
        Return the Delta Maintainability Model (DMM) metric value for the unit complexity property.

        It represents the proportion (between 0.0 and 1.0) of maintainability improving
        change, when considering the cyclomatic complexity of the modified methods.

        It rewards (value close to 1.0) modifications to low-risk (low complexity) methods,
        or spliting risky (highly complex) ones.
        It penalizes (value close to 0.0) working on methods that remain complex
        or get more complex.

        :return: The DMM value (between 0.0 and 1.0) for method complexity in this commit.
                 or None if none of the programming languages in the commit are supported.
        """
        return self._delta_maintainability(DMMProperty.UNIT_COMPLEXITY)

    @property
    def dmm_unit_interfacing(self) -> Optional[float]:
        """
        Return the Delta Maintainability Model (DMM) metric value for the unit interfacing property.

        It represents the proportion (between 0.0 and 1.0) of maintainability improving
        change, when considering the interface (number of parameters) of the modified methods.

        It rewards (value close to 1.0) modifications to low-risk (with  few parameters) methods,
        or spliting risky (with many parameters) ones.
        It penalizes (value close to 0.0) working on methods that continue to have
        or are extended with too many parameters.

        :return: The dmm value (between 0.0 and 1.0) for method interfacing in this commit.
                  or None if none of the programming languages in the commit are supported.
       """
        return self._delta_maintainability(DMMProperty.UNIT_INTERFACING)

    def _delta_maintainability(self, dmm_prop: DMMProperty) -> Optional[float]:
        """
        Compute the Delta Maintainability Model (DMM) value for the given risk predicate.
        The DMM value is computed as the proportion of good change in the commit:
        Good changes: Adding low risk code or removing high risk codee.
        Bad changes: Adding high risk code or removing low risk code.

        :param dmm_prop: Property indicating the type of risk
        :return: dmm value (between 0.0 and 1.0) for the property represented in the property.
        """
        delta_profile = self._delta_risk_profile(dmm_prop)
        if delta_profile:
            (delta_low, delta_high) = delta_profile
            return self._good_change_proportion(delta_low, delta_high)
        return None

    def _delta_risk_profile(self, dmm_prop: DMMProperty) -> Optional[Tuple[int, int]]:
        """
        Return the delta risk profile of this commit, which a pair (dv1, dv2), where
        dv1 is the total change in volume (lines of code) of low risk methods, and
        dv2 is the total change in volume of the high risk methods.

        :param dmm_prop: Property indicating the type of risk
        :return: total delta risk profile for this commit.
        """
        supported_modifications = [mod for mod in self.modifications if mod.language_supported]
        if supported_modifications:
            deltas = [mod._delta_risk_profile(dmm_prop) for mod in supported_modifications]
            delta_low = sum(dlow for (dlow, dhigh) in deltas)
            delta_high = sum(dhigh for (dlow, dhigh) in deltas)
            return delta_low, delta_high
        return None

    @staticmethod
    def _good_change_proportion(low_risk_delta: int, high_risk_delta: int) -> Optional[float]:
        """
        Given a delta risk profile, compute the proportion of "good" change in the total change.
        Increasing low risk code, or decreasing high risk code, is considered good.
        Other types of changes are considered not good.

        :return: proportion of good change in total change, or None if the total change is zero.
        """
        bad_change, good_change = (0, 0)

        if low_risk_delta >= 0:
            good_change = low_risk_delta
        else:
            bad_change = abs(low_risk_delta)
        if high_risk_delta >= 0:
            bad_change += high_risk_delta
        else:
            good_change += abs(high_risk_delta)

        assert good_change >= 0 and bad_change >= 0

        total_change = good_change + bad_change
        if total_change == 0:
            proportion = None
        else:
            proportion = good_change / total_change
            assert 0.0 <= proportion <= 1.0

        return proportion

    @staticmethod
    def _from_change_to_modification_type(diff: Diff):
        if diff.new_file:
            return ModificationType.ADD
        if diff.deleted_file:
            return ModificationType.DELETE
        if diff.renamed_file:
            return ModificationType.RENAME
        if diff.a_blob and diff.b_blob and diff.a_blob != diff.b_blob:
            return ModificationType.MODIFY

        return ModificationType.UNKNOWN

    def __eq__(self, other):
        if not isinstance(other, Commit):
            return NotImplemented
        if self is other:
            return True

        return self.__dict__ == other.__dict__
