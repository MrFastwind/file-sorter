from typing import List


class InvalidPattern(ValueError):
    def __init__(self, tags: List[str]) -> None:
        super().__init__("Tags not valid: " + ", ".join(tags))
