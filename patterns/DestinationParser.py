import re
from pathlib import Path
from typing import Callable, Dict, List

from patterns.PatternExceptions import InvalidPattern


class DestinationParser:
    valid_tags: Dict[str, Callable[[Path], Path]] = {
        "name": lambda file: file.stem,
        "parent": lambda file: file.parent,
        "ext": lambda file: file.suffix,
    }

    @classmethod
    def parse_file(cls, file: Path, pattern: str) -> Path:
        groups = re.findall(r"%(.*)%", pattern)
        cls.__check_groups(groups)
        ## replace valid tags
        for tag in cls.valid_tags:
            pattern = pattern.replace("%" + tag + "%", cls.valid_tags[tag](file))

        return pattern

    @classmethod
    def __check_groups(cls, groups: List[str]) -> bool:
        invalid_tags = [group for group in groups if group not in cls.valid_tags]
        if len(invalid_tags) > 0:
            raise InvalidPattern(invalid_tags)
        return True
