# Copyright 2018 Davide Spadini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module contains all the classes regarding a specific commit, such as
Commit, Modification,
ModificationType and Method.
"""
import logging
from _datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Set, Dict, Tuple, Optional

import hashlib

import lizard
import lizard_languages
from git import Diff, Git, NULL_TREE
from git.objects import Commit as GitCommit

from pydriller.domain.developer import Developer

logger = logging.getLogger(__name__)


class ModificationType(Enum):
    """
    Type of Modification. Can be ADD, COPY, RENAME, DELETE, MODIFY or UNKNOWN.
    """

    ADD = 1
    COPY = 2
    RENAME = 3
    DELETE = 4
    MODIFY = 5
    UNKNOWN = 6


class DMMProperty(Enum):
    """
    Maintainability properties of the Delta Maintainability Model.
    """

    UNIT_SIZE = 1
    UNIT_COMPLEXITY = 2
    UNIT_INTERFACING = 3


class Method:
    """
    This class represents a method in a class. Contains various information
    extracted through Lizard.
    """

    def __init__(self, func):
        """
        Initialize a method object. This is calculated using Lizard: it parses
        the source code of all the modifications in a commit, extracting
        information of the methods contained in the file (if the file is a
        source code written in one of the supported programming languages).
        """

        self.name = func.name
        self.long_name = func.long_name
        self.filename = func.filename
        self.nloc = func.nloc
        self.complexity = func.cyclomatic_complexity
        self.token_count = func.token_count
        self.parameters = func.parameters
        self.start_line = func.start_line
        self.end_line = func.end_line
        self.fan_in = func.fan_in
        self.fan_out = func.fan_out
        self.general_fan_out = func.general_fan_out
        self.length = func.length
        self.top_nesting_level = func.top_nesting_level

    def __eq__(self, other):
        return self.name == other.name and self.parameters == other.parameters

    def __hash__(self):
        # parameters are used in hashing in order to
        # prevent collisions when overloading method names
        return hash(
            (
                "name",
                self.name,
                "long_name",
                self.long_name,
                "params",
                (x for x in self.parameters),
            )
        )

    UNIT_SIZE_LOW_RISK_THRESHOLD = 15
    """
    Threshold used in the Delta Maintainability Model to establish whether a method
    is low risk in terms of its size.
    The procedure to obtain the threshold is described in the
    :ref:`PyDriller documentation <Properties>`.
    """

    UNIT_COMPLEXITY_LOW_RISK_THRESHOLD = 5
    """
    Threshold used in the Delta Maintainability Model to establish whether a method
    is low risk in terms of its cyclomatic complexity.
    The procedure to obtain the threshold is described in the
    :ref:`PyDriller documentation <Properties>`.
    """

    UNIT_INTERFACING_LOW_RISK_THRESHOLD = 2
    """
    Threshold used in the Delta Maintainability Model to establish whether a method
    is low risk in terms of its interface.
    The procedure to obtain the threshold is described in the
    :ref:`PyDriller documentation <Properties>`.
    """

    def is_low_risk(self, dmm_prop: DMMProperty) -> bool:
        """
        Predicate indicating whether this method is low risk in terms of
        the given property.

        :param dmm_prop: Property according to which this method is considered risky.
        :return: True if and only if the method is considered low-risk w.r.t. this property.
        """
        if dmm_prop is DMMProperty.UNIT_SIZE:
            return self.nloc <= Method.UNIT_SIZE_LOW_RISK_THRESHOLD
        if dmm_prop is DMMProperty.UNIT_COMPLEXITY:
            return self.complexity <= Method.UNIT_COMPLEXITY_LOW_RISK_THRESHOLD
        assert dmm_prop is DMMProperty.UNIT_INTERFACING
        return (
            len(self.parameters) <= Method.UNIT_INTERFACING_LOW_RISK_THRESHOLD
        )


class ModifiedFile:
    """
    This class contains information regarding a modified file in a commit.
    """

    def __init__(
        self,
        old_path: Optional[str],
        new_path: Optional[str],
        change_type: ModificationType,
        diff_and_sc: Dict[str, str],
    ):
        """
        Initialize a modified file. A modified file carries on information
        regarding the changed file. Normally, you shouldn't initialize a new
        one.
        """
        self._old_path = Path(old_path) if old_path is not None else None
        self._new_path = Path(new_path) if new_path is not None else None
        self.change_type = change_type
        self.diff = diff_and_sc["diff"]
        self.source_code = diff_and_sc["source_code"]
        self.source_code_before = diff_and_sc["source_code_before"]

        self._nloc = None
        self._complexity = None
        self._token_count = None
        self._function_list: List[Method] = []
        self._function_list_before: List[Method] = []

    def __hash__(self):
        """
        Implements hashing similar as Git would do it. Alternatively, if the
        object had the hash of th Git Blob, one could use that directly.

        :return: int hash
        """
        string = f"{self.change_type.name} {self.new_path} {self.source_code}"
        return hash(hashlib.sha256(string.encode("utf-8")).hexdigest())

    @property
    def added_lines(self) -> int:
        """
        Return the total number of added lines in the file.

        :return: int lines_added
        """
        added_lines = 0
        for line in self.diff.replace("\r", "").split("\n"):
            if line.startswith("+") and not line.startswith("+++"):
                added_lines += 1
        return added_lines

    @property
    def deleted_lines(self):
        """
        Return the total number of deleted lines in the file.

        :return: int lines_deleted
        """
        deleted_lines = 0
        for line in self.diff.replace("\r", "").split("\n"):
            if line.startswith("-") and not line.startswith("---"):
                deleted_lines += 1
        return deleted_lines

    @property
    def old_path(self):
        """
        Old path of the file. Can be None if the file is added.

        :return: str old_path
        """
        if self._old_path is not None:
            return str(self._old_path)
        return None

    @property
    def new_path(self):
        """
        New path of the file. Can be None if the file is deleted.

        :return: str new_path
        """
        if self._new_path is not None:
            return str(self._new_path)
        return None

    @property
    def filename(self) -> str:
        """
        Return the filename. Given a path-like-string (e.g.
        "/Users/dspadini/pydriller/myfile.py") returns only the filename
        (e.g. "myfile.py")

        :return: str filename
        """
        if self._new_path is not None and str(self._new_path) != "/dev/null":
            path = self._new_path
        else:
            assert self._old_path
            path = self._old_path

        return path.name

    @property
    def language_supported(self) -> bool:
        """
        Return whether the language used in the modification can be analyzed by Pydriller.
        Languages are derived from the file  extension.
        Supported languages are those supported by Lizard.

        :return: True iff language of this Modification can be analyzed.
        """
        return lizard_languages.get_reader_for(self.filename) is not None

    @property
    def nloc(self) -> Optional[int]:
        """
        Calculate the LOC of the file.

        :return: LOC of the file
        """
        self._calculate_metrics()
        return self._nloc

    @property
    def complexity(self) -> Optional[int]:
        """
        Calculate the Cyclomatic Complexity of the file.

        :return: Cyclomatic Complexity of the file
        """
        self._calculate_metrics()
        return self._complexity

    @property
    def token_count(self) -> Optional[int]:
        """
        Calculate the token count of functions.

        :return: token count
        """
        self._calculate_metrics()
        return self._token_count

    @property
    def diff_parsed(self) -> Dict[str, List[Tuple[int, str]]]:
        """
        Returns a dictionary with the added and deleted lines.
        The dictionary has 2 keys: "added" and "deleted", each containing the
        corresponding added or deleted lines. For both keys, the value is a
        list of Tuple (int, str), corresponding to (number of line in the file,
        actual line).

        :return: Dictionary
        """
        lines = self.diff.split("\n")
        modified_lines = {
            "added": [],
            "deleted": [],
        }  # type: Dict[str, List[Tuple[int, str]]]

        count_deletions = 0
        count_additions = 0

        for line in lines:
            line = line.rstrip()
            count_deletions += 1
            count_additions += 1

            if line.startswith("@@"):
                count_deletions, count_additions = self._get_line_numbers(line)

            if line.startswith("-"):
                modified_lines["deleted"].append((count_deletions, line[1:]))
                count_additions -= 1

            if line.startswith("+"):
                modified_lines["added"].append((count_additions, line[1:]))
                count_deletions -= 1

            if line == r"\ No newline at end of file":
                count_deletions -= 1
                count_additions -= 1

        return modified_lines

    @staticmethod
    def _get_line_numbers(line):
        token = line.split(" ")
        numbers_old_file = token[1]
        numbers_new_file = token[2]
        delete_line_number = (
            int(numbers_old_file.split(",")[0].replace("-", "")) - 1
        )
        additions_line_number = int(numbers_new_file.split(",")[0]) - 1
        return delete_line_number, additions_line_number

    @property
    def methods(self) -> List[Method]:
        """
        Return the list of methods in the file. Every method
        contains various information like complexity, loc, name,
        number of parameters, etc.

        :return: list of methods
        """
        self._calculate_metrics()
        return self._function_list

    @property
    def methods_before(self) -> List[Method]:
        """
        Return the list of methods in the file before the
        change happened. Each method will have all specific
        info, e.g. complexity, loc, name, etc.

        :return: list of methods
        """
        self._calculate_metrics(include_before=True)
        return self._function_list_before

    @property
    def changed_methods(self) -> List[Method]:
        """
        Return the list of methods that were changed. This analysis
        is more complex because Lizard runs twice: for methods before
        and after the change

        :return: list of methods
        """
        new_methods = self.methods
        old_methods = self.methods_before
        added = self.diff_parsed["added"]
        deleted = self.diff_parsed["deleted"]

        methods_changed_new = {
            y
            for x in added
            for y in new_methods
            if y.start_line <= x[0] <= y.end_line
        }
        methods_changed_old = {
            y
            for x in deleted
            for y in old_methods
            if y.start_line <= x[0] <= y.end_line
        }

        return list(methods_changed_new.union(methods_changed_old))

    @staticmethod
    def _risk_profile(
        methods: List[Method], dmm_prop: DMMProperty
    ) -> Tuple[int, int]:
        """
        Return the risk profile of the set of methods, with two bins: risky, or non risky.
        The risk profile is a pair (v_low, v_high), where
        v_low is the volume of the low risk methods in the list, and
        v_high is the volume of the high risk methods in the list.

        :param methods: List of methods for which risk profile is to be determined
        :param dmm_prop: Property indicating the type of risk
        :return: total risk profile for methods according to property.
        """
        low = sum([m.nloc for m in methods if m.is_low_risk(dmm_prop)])
        high = sum([m.nloc for m in methods if not m.is_low_risk(dmm_prop)])
        return low, high

    def _delta_risk_profile(self, dmm_prop: DMMProperty) -> Tuple[int, int]:
        """
        Return the delta risk profile of this commit, which a pair (dv1, dv2), where
        dv1 is the total change in volume (lines of code) of low risk methods, and
        dv2 is the total change in volume of the high risk methods.

        :param dmm_prop: Property indicating the type of risk
        :return: total delta risk profile for this property.
        """
        assert self.language_supported
        low_before, high_before = self._risk_profile(
            self.methods_before, dmm_prop
        )
        low_after, high_after = self._risk_profile(self.methods, dmm_prop)
        return low_after - low_before, high_after - high_before

    def _calculate_metrics(self, include_before=False):
        """
        :param include_before: either to compute the metrics
        for source_code_before, i.e. before the change happened
        """
        if not self.language_supported:
            return

        if self.source_code and self._nloc is None:
            analysis = lizard.analyze_file.analyze_source_code(
                self.filename, self.source_code
            )
            self._nloc = analysis.nloc
            self._complexity = analysis.CCN
            self._token_count = analysis.token_count

            for func in analysis.function_list:
                self._function_list.append(Method(func))

        if (
            include_before
            and self.source_code_before
            and not self._function_list_before
        ):
            anal = lizard.analyze_file.analyze_source_code(
                self.filename, self.source_code_before
            )

            self._function_list_before = [Method(x) for x in anal.function_list]

    def __eq__(self, other):
        if not isinstance(other, ModifiedFile):
            return NotImplemented
        if self is other:
            return True
        return self.__dict__ == other.__dict__


class Commit:
    """
    Class representing a Commit. Contains all the important information such
    as hash, author, dates, and modified files.
    """

    def __init__(self, commit: GitCommit, conf) -> None:
        """
        Create a commit object.

        :param commit: GitPython Commit object
        :param conf: Configuration class
        """
        self._c_object = commit

        self._modified_files = None
        self._branches = None
        self._conf = conf

    def __hash__(self):
        """
        Since already used in Git for identification use the SHA of the commit
        as hash value.

        :return: int hash
        """
        # Unfortunately, the Git hash cannot be used for the Python object
        # directly. The documentation says it "should" return an integer
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        # but I just learned it **has** to return one.
        return hash(self._c_object.hexsha)

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
        return Developer(
            self._c_object.author.name, self._c_object.author.email
        )

    @property
    def committer(self) -> Developer:
        """
        Return the committer of the commit as a Developer object.

        :return: committer
        """
        return Developer(
            self._c_object.committer.name, self._c_object.committer.email
        )

    @property
    def project_name(self) -> str:
        """
        Return the project name.

        :return: project name
        """
        return Path(self._conf.get("path_to_repo")).name

    @property
    def project_path(self) -> str:
        """
        Return the absolute path of the project.

        :return: project path
        """
        return str(Path(self._conf.get("path_to_repo")))

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
        return int(self._c_object.author_tz_offset)

    @property
    def committer_timezone(self) -> int:
        """
        Author timezone expressed in seconds from epoch.

        :return: int timezone
        """
        return int(self._c_object.committer_tz_offset)

    @property
    def msg(self) -> str:
        """
        Return commit message.

        :return: str commit_message
        """
        return str(self._c_object.message.strip())

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
    def insertions(self) -> int:
        """
        Return the number of added lines in the commit (as shown from --shortstat).

        :return: int insertion lines
        """
        return self._c_object.stats.total["insertions"]

    @property
    def deletions(self) -> int:
        """
        Return the number of deleted lines in the commit (as shown from --shortstat).

        :return: int deletion lines
        """
        return self._c_object.stats.total["deletions"]

    @property
    def lines(self) -> int:
        """
        Return the number of modified lines in the commit (as shown from --shortstat).

        :return: int insertion + deletion lines
        """
        return self._c_object.stats.total["lines"]

    @property
    def files(self) -> int:
        """
        Return the number of modified files of the commit (as shown from --shortstat).

        :return: int modified files number
        """
        return self._c_object.stats.total["files"]

    @property
    def modified_files(self) -> List[ModifiedFile]:
        """
        Return a list of modified files. The list is empty if the commit is
        a merge commit. For more info on this, see
        https://haacked.com/archive/2014/02/21/reviewing-merge-commits/ or
        https://github.com/ishepard/pydriller/issues/89#issuecomment-590243707

        :return: List[Modification] modifications
        """
        if self._modified_files is None:
            self._modified_files = self._get_modified_files()

        assert self._modified_files is not None
        return self._modified_files

    def _get_modified_files(self):
        options = {}
        if self._conf.get("histogram"):
            options["histogram"] = True

        if self._conf.get("skip_whitespaces"):
            options["w"] = True

        if len(self.parents) == 1:
            # the commit has a parent
            diff_index = self._c_object.parents[0].diff(
                self._c_object, create_patch=True, **options
            )
        elif len(self.parents) > 1:
            # if it's a merge commit, the modified files of the commit are the
            # conflicts. This because if the file is not in conflict,
            # pydriller will visit the modification in one of the previous
            # commits. However, parsing the output of a combined diff (that
            # returns the list of conflicts) is challenging: so, right now,
            # I will return an empty array, in the meanwhile I will try to
            # find a way to parse the output.
            # c_git = Git(str(self.project_path))
            # d = c_git.diff_tree("--cc", commit.hexsha, '-r', '--abbrev=40',
            #                     '--full-index', '-M', '-p', '--no-color')
            diff_index = []
        else:
            # this is the first commit of the repo. Comparing it with git
            # NULL TREE
            diff_index = self._c_object.diff(
                NULL_TREE, create_patch=True, **options
            )

        return self._parse_diff(diff_index)

    def _parse_diff(self, diff_index) -> List[ModifiedFile]:
        modified_files_list = []
        for diff in diff_index:
            old_path = diff.a_path
            new_path = diff.b_path
            change_type = self._from_change_to_modification_type(diff)

            diff_and_sc = {
                "diff": self._get_decoded_str(diff.diff),
                "source_code_before": self._get_decoded_sc_str(diff.a_blob),
                "source_code": self._get_decoded_sc_str(diff.b_blob),
            }

            modified_files_list.append(
                ModifiedFile(old_path, new_path, change_type, diff_and_sc)
            )

        return modified_files_list

    def _get_decoded_str(self, diff):
        try:
            return diff.decode("utf-8", "ignore")
        except (AttributeError, ValueError):
            logger.debug(
                "Could not load the diff of a " "file in commit %s",
                self._c_object.hexsha,
            )
            return None

    def _get_decoded_sc_str(self, diff):
        try:
            return diff.data_stream.read().decode("utf-8", "ignore")
        except (AttributeError, ValueError):
            logger.debug(
                "Could not load source code of a " "file in commit %s",
                self._c_object.hexsha,
            )
            return None

    @property
    def in_main_branch(self) -> bool:
        """
        Return True if the commit is in the main branch, False otherwise.

        :return: bool in_main_branch
        """
        return self._conf.get("main_branch") in self.branches

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
        c_git = Git(str(self._conf.get("path_to_repo")))
        branches = set()
        args = ["--contains", self.hash]
        if self._conf.get("include_remotes"):
            args = ["-r"] + args
        if self._conf.get("include_refs"):
            args = ["-a"] + args
        for branch in set(c_git.branch(*args).split("\n")):
            branches.add(branch.strip().replace("* ", ""))
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

    def _delta_risk_profile(
        self, dmm_prop: DMMProperty
    ) -> Optional[Tuple[int, int]]:
        """
        Return the delta risk profile of this commit, which a pair (dv1, dv2), where
        dv1 is the total change in volume (lines of code) of low risk methods, and
        dv2 is the total change in volume of the high risk methods.

        :param dmm_prop: Property indicating the type of risk
        :return: total delta risk profile for this commit.
        """
        supported_modifications = [
            mod for mod in self.modified_files if mod.language_supported
        ]
        if supported_modifications:
            deltas = [
                mod._delta_risk_profile(dmm_prop)
                for mod in supported_modifications
            ]
            delta_low = sum(dlow for (dlow, dhigh) in deltas)
            delta_high = sum(dhigh for (dlow, dhigh) in deltas)
            return delta_low, delta_high
        return None

    @staticmethod
    def _good_change_proportion(
        low_risk_delta: int, high_risk_delta: int
    ) -> Optional[float]:
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
