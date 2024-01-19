import fnmatch
from logging import Logger
from pathlib import Path
import re
from typing import Protocol


class Pattern(Protocol):
    def match(self, file: Path, pattern: str) -> bool:
        ...


class GlobPattern:
    @classmethod
    def match(cls, file: Path, pattern: str) -> bool:
        return fnmatch.fnmatchcase(file, filter)


class RegexPattern:
    @classmethod
    def match(cls, file: Path, pattern: str) -> bool:
        return re.match(filter, str(file)) == True

    @classmethod
    def is_regex(cls, pattern: str) -> bool:
        try:
            re.compile(pattern)
            return True
        except re.error:
            Logger.debug(f"filter is not a Regex: {pattern}")
        return False
