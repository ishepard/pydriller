import subprocess
from abc import ABC, abstractmethod
from pydriller.domain.developer import Developer
from typing import Optional, Tuple


class DeveloperFactory(ABC):

    @abstractmethod
    def get_developer(self, name: Optional[str] = None, email: Optional[str] = None) -> Developer:
        pass


class DefaultDeveloperFactory(DeveloperFactory):

    def get_developer(self, name: Optional[str] = None, email: Optional[str] = None) -> Developer:
        return Developer(name, email)


class MailmapDeveloperFactory(DeveloperFactory):

    def __init__(self, conf):
        self.check_mailmap_cache = {}
        self._conf = conf

    def _run_check_mailmap(self, name: Optional[str] = None, email: Optional[str] = None) -> Tuple[str, str]:
        """ Call `git check-mailmap` to map names and emails of `Developer`s to canonical values.

        This method wraps a call to the `git-check-mailmap` binary. Given a name and email address of an author or
        committer, e.g., in the form `"My Name" "<me@work.com>"` it displays canonical names and email addresses based
        on entries provided in a repositories `.mailmap` file.
        The tool is documented here: https://git-scm.com/docs/git-check-mailmap/2.31.0

        In case anything goes wrong while calling `git-check-mailmap` the method returns the input values for name and
        email. This is inline with the behavior of `git-check-mailmap`, see documentation.
        """

        # In future, once Git version >= 2.47 is installed by most of pydriller users, the call might be refactored to
        # use the `--mailmap-file` option so that PyDriller users can specify `.mailmap` files outside of repositories
        # for analysis.
        result = subprocess.run(
            ["git", "-C", f"{self._conf.get('path_to_repo')}", "check-mailmap", f"{name} <{email}>"],
            capture_output=True,
            text=True
        )

        if result.stdout:
            # I believe string splitting is easier to understand than a regular expression here
            if result.stdout.startswith("<"):
                map_name = ""
                map_email = result.stdout[1:-2]
            else:
                map_name, map_email = result.stdout.split(" <")
                map_email = map_email[:-2]
        elif result.stderr:
            # This is to make it robust. In case anything goes wrong, go with the knowledge
            # that we have about the author or committer
            return str(name), str(email)
        return map_name, map_email

    def get_developer(self, name: Optional[str] = None, email: Optional[str] = None) -> Developer:
        """ Get canonical names and emails for a `Developer`.

        If for a `Developer` name and email where never mapped to canonical values by calling the `git-check-mailmap`
        binary, then call the binary and cache the respective results in a dictionary to speed up later look ups.
        Otherwise, receive canonical name and email values directly from the cache.

        Caching results in a dictionary uses some RAM but I believe there are no repositories with so many authors that
        this will pose an issue on modern computers.
        """
        developer = Developer(name, email)
        if cached_developer := self.check_mailmap_cache.get(developer):
            return cached_developer

        try:
            map_name, map_email = self._run_check_mailmap(name, email)
            mapped_developer = Developer(map_name, map_email)
            self.check_mailmap_cache[developer] = mapped_developer
            return mapped_developer
        except Exception:
            return developer
