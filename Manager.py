import logging as Logger
from pathlib import Path
from typing import Callable, Generator, List
from action import ActionInvoker
from action.Action import Action
from rule.Rules import Rule


class FolderManager:
    def setRules(self, rules: List[Rule]):
        self._rules = rules

    def setFolder(self, path: Path):
        self._path = path

    def setInvoker(self, invoker: ActionInvoker):
        self._invoker = invoker

    def run(self):
        if not self._path or not self._invoker:
            Logger.info("No path or invoker set")
            return
        files = self.searchInFolder()
        rules = iter(self._rules)

        try:
            while True:
                rule = next(rules)
                actions = rule.handle(files)
                if actions:
                    for action in actions:
                        self._invoker.execute(action)
                        files.pop(action.file)
        except StopIteration:
            pass

        report = self._invoker.report()

    def searchInFolder(self) -> List[Path]:
        return [item for item in self._path.rglob("*.*")]

    def applyAction(self, file: Path, action: Action) -> bool:
        return action.apply(file)
