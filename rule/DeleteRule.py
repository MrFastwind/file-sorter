from pathlib import Path
from typing import List, Set
from action.Action import Action
from patterns.Pattern import Pattern
from rule.Rule import Rule


class DeleteRule(Rule):
    def __init__(self, filter: Pattern):
        self._filter = filter

    def handle(self, files: Set[Path]) -> List[Action]:
        return [
            Action.delete(file) for file in files if self._filter.match(self._filter)
        ]
