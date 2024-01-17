from Action import Action
from Rule import Rule
from pathlib import Path
from typing import Dict, Iterator, Set


class ChainRule:
    def __init__(self) -> None:
        self.rules: Set[Rule] = {}

    def addRule(self, rule: Rule):
        self.rules.add(rule)

    def removeRule(self, rule: Rule):
        self.rules.remove(rule)

    def __iter__(self):
        return self.rules.__iter__()
