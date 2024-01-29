from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import Callable, List, Set, Protocol, Type

from patterns.Pattern import Pattern
from action.Action import Action, DeleteAction, KeepAction, MoveAction
from patterns.DestinationParser import DestinationParser


class Rule(Protocol):
    def handle(self, files: Set[Path]) -> List[Action]:
        """
        Handle the given set of files and return a list of actions.
        :param files: a set of Path objects representing the files to be handled
        :return: a list of Action objects representing the actions to be taken
        """
        ...


class MoveRule(Rule):
    def __init__(self, filter: Pattern, destination: str | Path):
        """
        Initialize the object with the provided filter pattern and destination.

        Parameters:
            filter (Pattern): The filter pattern to be used.
            destination (str): The destination string.

        Returns:
            None
        """
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
        """
        Initializes the object with the given filter and delegate.

        :param filter: The filter pattern to be used.
        :type filter: Pattern
        :param delegate: The delegate function to generate actions based on the path.
        :type delegate: Callable[[Path], Type[Action]]
        """
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
