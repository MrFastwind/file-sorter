from dataclasses import dataclass
from pathlib import Path
from typing import List

from rule.Rule import Rule


@dataclass
class Site:
    path: Path
    enabled: bool
    rules: List[Rule] = []
