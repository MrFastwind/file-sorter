from multiprocessing.pool import ThreadPool
from threading import Lock
from action.Action import Action


from typing import Protocol


class ActionInvoker(Protocol):
    def __init__(self) -> None:
        ...

    def execute(self, action: Action):
        ...

    def report(self) -> str:
        ...


class ExecutionerActionInvoker(ActionInvoker):
    def __init__(self, executor: ThreadPool = ThreadPool(4)) -> None:
        self._executor = executor
        self._mutex = Lock()

    def execute(self, action: Action):
        self._executor.apply_async(
            action.apply,
            callback=lambda x: self.__add_report(x.report()),
            error_callback=lambda x: self.__add_report(x.report()),
        )

    def __add_report(self, report: str):
        with self._mutex:
            self._reports.append(report)

    def report(self) -> str:
        with self._mutex:
            return self._reports
