from enum import Enum


class ModificationType(Enum):
    ADD = 1,
    COPY = 2,
    RENAME = 3,
    DELETE = 4,
    MODIFY = 5
