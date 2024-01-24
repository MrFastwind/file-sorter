from multiprocessing.pool import AsyncResult, ThreadPool
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

    def close(self):
        ...


class ExecutionerActionInvoker(ActionInvoker):
    def __init__(self, executor: ThreadPool = ThreadPool(4)) -> None:
        self._executor = executor
        self._mutex = Lock()
        self._reports = []
        self._tasks = 0

    def execute(self, action: Action):
        with self._mutex:
            self.results.append(
                self._executor.apply_async(
                    action.apply,
                    callback=lambda x: self.__add_report(x.report()),
                    error_callback=lambda x: self.__add_report(x.report()),
                )
            )
            self._tasks += 1

    def close(self):
        while self._tasks != 0:
            ...
        with self._mutex:
            self._executor.close()

    def __add_report(self, report: str):
        with self._mutex:
            self._reports.append(report)
            self.remaining -= 1

    def report(self) -> str:
        with self._mutex:
            return self._reports
