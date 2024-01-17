from pathlib import Path
from typing import Callable, List
from Action import Action
from ChainRule import ChainRule
from Rule import Rule


class Manager:
    def setRuleChain(self, chain: ChainRule):
        self._chain = chain

    def run(self):
        files = self.searchInFolder()
        rules = iter(self._chain)

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
