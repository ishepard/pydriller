from domain.modification_type import ModificationType
import re
import os


class Modification:
    def __init__(self, old_path: str, new_path: str, change_type: ModificationType, diff: str, source_code: str):
        """
        Initialize a modification. A modification carries on information regarding
        the changed file.
        :param old_path: old path of the file (can be null if the file is added)
        :param new_path: new path of the file (can be null if the file is deleted)
        :param change_type: type of the change
        :param diff: diff of the change
        :param source_code: source code of the file (can be null if the file is deleted)
        """

        self.old_path = old_path
        self.new_path = new_path
        self.change_type = change_type
        self.diff = diff
        self.source_code = source_code
        self.added = 0
        self.removed = 0

        for line in diff.replace('\r', '').split("\n"):
            if line.startswith('+') and not line.startswith('+++'):
                self.added += 1
            if line.startswith('-') and not line.startswith('---'):
                self.removed += 1

    def filename_ends_with(self, suffix: str) -> bool:
        return self.new_path.lower().endswith(suffix.lower())

    def filename_matches(self, regex: str) -> bool:
        pattern = re.compile(regex)
        return pattern.match(self.new_path.lower())

    def get_filename(self) -> str:
        if self.new_path is not None and self.new_path != "/dev/null":
            path = self.new_path
        else:
            path = self.old_path

        if os.sep not in path:
            return path

        filename = path.split(os.sep)
        return filename[-1]

    def __eq__(self, other):
        if not isinstance(other, Modification):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return (
            'Old Path: {}\n'.format(self.old_path) +
            'New Path: {}\n'.format(self.new_path) +
            'Type: {}\n'.format(self.change_type.name) +
            'Diff: {}\n'.format(self.diff) +
            'Source code: {}\n'.format(self.source_code)
        )