from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import Callable, List, Set, Protocol, Type

from patterns.Pattern import Pattern
from action.Action import Action, DeleteAction, KeepAction, MoveAction
from patterns.DestinationParser import DestinationParser


class Rule(Protocol):
    def handle(self, files: Set[Path]) -> List[Action]:
        ...


class MoveRule(Rule):
    def __init__(self, filter: Pattern, destination: str):
        self.filter: Pattern = filter
        self.destination = destination

    def handle(self, files: Set[Path]) -> List[Action]:
        actions = []
        pattern: Pattern = self.filter

        for file in files:
            if pattern.match(file):
                destination = Path(self.destination)

                if destination.is_file():
                    actions.append(MoveAction(file, self.destination))
                    continue

                if destination.is_dir():
                    actions.append(MoveAction(file, self.destination / file.name))
                    continue

                actions.append(
                    MoveAction(
                        file, DestinationParser.parse_file(file, self.destination)
                    )
                )


class DelegateRule(Rule):
    def __init__(self, filter: Pattern, delegate: Callable[[Path], Type[Action]]):
        self._filter = filter
        self._actionGenerator = delegate

    def handle(self, files: Set[Path]) -> List[Action]:
        return [
            self._actionGenerator(file)
            for file in files
            if self._filter.match(self._filter)
        ]


class DeleteRule(DelegateRule):
    def __init__(self, filter: Pattern):
        super().__init__(filter, DeleteAction)


class KeepRule(Rule):
    def __init__(self, filter: Pattern):
        super().__init__(filter, KeepAction)


class TrashRule(Rule):
    def __init__(self, filter: Pattern):
        super().__init__(filter, KeepAction)
