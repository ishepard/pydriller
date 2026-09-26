# pylint: disable=C0111
from .domain.commit import Commit, ModifiedFile, ModificationType # noqa
from .repository import Repository, Git    # noqa
from .git import ShallowRepositoryError    # noqa

__version__ = "2.12"
