from domain.modification_type import ModificationType
import re
import os


class Modification:
    def __init__(self, old_path: str, new_path: str, type: ModificationType, diff: str, source_code: str):
        self.old_path = old_path
        self.new_path = new_path
        self.type = type
        self.diff = diff
        self.source_code = source_code

        for line in diff.replace('\r', '').split("\n"):
            if line.startswith('+') and not line.startswith('+++'):
                self.added += 1
            if line.startswith('-') and not line.startswith('---'):
                self.removed += 1

    def was_deleted(self):
        return type == ModificationType.DELETE

    def filename_ends_with(self, suffix: str):
        return self.new_path.lower().endswith(suffix.lower())

    def filename_matches(self, regex: str):
        pattern = re.compile(regex)
        return pattern.match(self.new_path.lower())

    def get_filename(self):
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