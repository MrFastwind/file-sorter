from pathlib import Path
from typing import List, Set
from action.Action import Action, MoveAction
from patterns.DestinationParser import DestinationParser
from patterns.Pattern import GlobPattern, Pattern, RegexPattern
from rule.Rule import Rule


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
