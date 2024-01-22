import fnmatch
from logging import Logger
from pathlib import Path
import re
from typing import Protocol


class Pattern(Protocol):
    def match(self, file: Path) -> bool:
        ...


class GlobPattern:
    def __init__(self, filter: str):
        self._filter = filter

    def match(self, file: Path) -> bool:
        return fnmatch.fnmatchcase(file, self.filter)


class RegexPattern:
    def match(self, file: Path, pattern: str) -> bool:
        return re.match(filter, str(file)) == True

    def is_regex(self, pattern: str) -> bool:
        try:
            re.compile(pattern)
            return True
        except re.error:
            Logger.debug(f"filter is not a Regex pattern: {pattern}")
        return False
