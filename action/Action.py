from enum import Enum
import os
from pathlib import Path
from typing import List, Protocol
from attr import dataclass
from send2trash import send2trash


class ActionType(Enum):
    DELETE = 1
    KEEP = 2
    MOVE = 3
    TRASH = 4


class Action(Protocol):
    @property
    def file(self) -> Path:
        """
        Get the file path.

        Returns:
            Path: The file path.
        """
        ...

    @property
    def type(self) -> ActionType:
        """
        Returns the type of the action.

        :return: An ActionType enum representing the type of the action.
        :rtype: ActionType
        """
        ...

    def apply(self) -> bool:
        """
        Apply the changes made in this instance of the class.

        Returns:
            bool: True if the changes were successfully applied, False otherwise.
        """
        ...

    def report(self) -> str:
        """
        A function that generates the comment for the given function body.

        :param self: The instance of the class.
        :return: A string representing the function comment.
        :rtype: str
        """
        ...


class DeleteAction(Action):
    def __init__(self, file: Path):
        self._file = file

    @property
    def type(self) -> ActionType:
        return ActionType.DELETE

    @property
    def file(self):
        return self._file

    def apply(self) -> bool:
        if self.file.is_file():
            os.remove(self.file)
        elif self.file.is_dir():
            os.rmdir(self.file)
        else:
            return False
        return not self.file.exists()

    def report(self) -> str:
        return (
            f"Deleted {self.file}"
            if not self.file.exists()
            else f"Could not delete {self.file}"
        )


class KeepAction(Action):
    def __init__(self, file: Path):
        self._file = file

    @property
    def type(self) -> ActionType:
        return ActionType.KEEP

    @property
    def file(self):
        return self._file

    def apply(self) -> bool:
        return self.file.exists()

    def report(self) -> str:
        return (
            f"Kept {self.file}" if self.file.exists() else f"not existing {self.file}"
        )


class MoveAction(Action):
    def __init__(self, source: Path, destination: Path) -> None:
        super().__init__()
        self.destination = destination
        self.file = source
        self.moved = False

    @property
    def type(self) -> ActionType:
        return ActionType.MOVE

    @property
    def file(self):
        return self._file

    def apply(self) -> bool:
        if self.destination.exists():
            return False
        os.rename(self.file, self.destination)
        self.moved = self.destination.exists()
        return self.moved

    def report(self) -> str:
        return (
            f"Moved {self.file} to {self.destination}"
            if self.moved
            else f"Could not move {self.file}"
        )


class TrashAction(Action):
    def __init__(self, file: Path) -> None:
        self._file = file

    @property
    def type(self) -> ActionType:
        return ActionType.MOVE

    @property
    def file(self):
        return self._file

    def apply(self) -> bool:
        send2trash(self.file)
        return not self.file.exists()

    def report(self) -> str:
        return (
            f"Moved {self.file} to trash"
            if not self.file.exists()
            else f"Could not move {self.file}"
        )
