from pathlib import Path
from typing import Callable, List
from action.Action import Action
from rule.Rule import Rule


class Manager:
    def setRules(self, rules: List[Rule]):
        self._rules = rules

    def run(self):
        files = self.searchInFolder()
        rules = iter(self._rules)

        try:
            while True:
                rule = next(rules)
                actions = rule.handle(files)
                if actions:
                    for action in actions:
                        self.invoker.execute(action)
                        files.pop(action.file)
        except StopIteration:
            pass

        report = self.invoker.report()

    def applyAction(self, file: Path, action: Action) -> bool:
        return action.apply(file)
