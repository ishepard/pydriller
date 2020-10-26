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
from enum import Enum
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import lizard
import lizard_languages

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
        return hash(('name', self.name,
                     'long_name', self.long_name,
                     'params', (x for x in self.parameters)))

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
        return len(self.parameters) <= Method.UNIT_INTERFACING_LOW_RISK_THRESHOLD


class Modification:
    """
    This class contains information regarding a modified file in a commit.
    """

    def __init__(self, old_path: str, new_path: str,
                 change_type: ModificationType,
                 diff_and_sc: Dict[str, str]):
        """
        Initialize a modification. A modification carries on information
        regarding the changed file. Normally, you shouldn't initialize a new
        one.
        """
        self._old_path = Path(old_path) if old_path is not None else None
        self._new_path = Path(new_path) if new_path is not None else None
        self.change_type = change_type
        self.diff = diff_and_sc['diff']
        self.source_code = diff_and_sc['source_code']
        self.source_code_before = diff_and_sc['source_code_before']

        self._nloc = None
        self._complexity = None
        self._token_count = None
        self._function_list = []  # type: List[Method]
        self._function_list_before = []  # type: List[Method]

    @property
    def added(self) -> int:
        """
        Return the total number of added lines in the file.

        :return: int lines_added
        """
        added = 0
        for line in self.diff.replace('\r', '').split("\n"):
            if line.startswith('+') and not line.startswith('+++'):
                added += 1
        return added

    @property
    def removed(self):
        """
        Return the total number of deleted lines in the file.

        :return: int lines_deleted
        """
        removed = 0
        for line in self.diff.replace('\r', '').split("\n"):
            if line.startswith('-') and not line.startswith('---'):
                removed += 1
        return removed

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
        lines = self.diff.split('\n')
        modified_lines = {'added': [], 'deleted': []}  # type: Dict[str, List[Tuple[int, str]]]

        count_deletions = 0
        count_additions = 0

        for line in lines:
            line = line.rstrip()
            count_deletions += 1
            count_additions += 1

            if line.startswith('@@'):
                count_deletions, count_additions = self._get_line_numbers(line)

            if line.startswith('-'):
                modified_lines['deleted'].append((count_deletions, line[1:]))
                count_additions -= 1

            if line.startswith('+'):
                modified_lines['added'].append((count_additions, line[1:]))
                count_deletions -= 1

            if line == r'\ No newline at end of file':
                count_deletions -= 1
                count_additions -= 1

        return modified_lines

    @staticmethod
    def _get_line_numbers(line):
        token = line.split(" ")
        numbers_old_file = token[1]
        numbers_new_file = token[2]
        delete_line_number = int(numbers_old_file.split(",")[0].replace("-", "")) - 1
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
        added = self.diff_parsed['added']
        deleted = self.diff_parsed['deleted']

        methods_changed_new = {y for x in added for y in new_methods if
                               y.start_line <= x[0] <= y.end_line}
        methods_changed_old = {y for x in deleted for y in old_methods if
                               y.start_line <= x[0] <= y.end_line}

        return list(methods_changed_new.union(methods_changed_old))

    @staticmethod
    def _risk_profile(methods: List[Method], dmm_prop: DMMProperty) -> Tuple[int, int]:
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
        low_before, high_before = self._risk_profile(self.methods_before, dmm_prop)
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
            analysis = lizard.analyze_file.analyze_source_code(self.filename,
                                                               self.source_code)
            self._nloc = analysis.nloc
            self._complexity = analysis.CCN
            self._token_count = analysis.token_count

            for func in analysis.function_list:
                self._function_list.append(Method(func))

        if include_before and self.source_code_before and \
                not self._function_list_before:
            anal = lizard.analyze_file.analyze_source_code(
                self.filename, self.source_code_before)

            self._function_list_before = [
                Method(x) for x in anal.function_list]

    def __eq__(self, other):
        if not isinstance(other, Modification):
            return NotImplemented
        if self is other:
            return True
        return self.__dict__ == other.__dict__
