from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import List, Set, Protocol

from action.Action import Action


class Rule(Protocol):
    def handle(self, files: Set[Path]) -> List[Action]:
        ...
