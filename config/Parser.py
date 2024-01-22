from pathlib import Path
from typing import Dict, List, Protocol, Type
from config.Site import Site
from patterns.Pattern import GlobPattern, Pattern, RegexPattern
from rule.DeleteRule import DeleteRule

from rule.MoveRule import MoveRule
from rule.Rule import Rule


class Parser(Protocol):
    def parse(self, **kwargs) -> Type["Parser"]:
        pass


class PatternParser:
    def parse(self, filter: str) -> Type[Pattern]:
        if filter:
            if RegexPattern.is_regex(filter):
                return RegexPattern(filter)
            return GlobPattern(filter)

        raise ValueError("Invalid config format. Missing filter")


class RuleParser:
    @classmethod
    def parse(cls, type: str, **kwargs) -> Rule:
        if not type:
            raise ValueError("Invalid config format. Missing type")
        class_name = cls.__parseType(kwargs)

        ## try to crate a class with the type name = to obj_type, and use the attributes present inside obj
        return cls.instantiate_class(type, kwargs)

    @classmethod
    def __parseType(cls, class_name: str) -> Type[Rule]:
        # TODO: Implement Rules
        if class_name == "Move":
            return MoveRule
        if class_name == "Delete":
            return DeleteRule
        if class_name == "Keep":
            NotImplementedError("KeepRule not implemented yet")
        if class_name == "Trash":
            NotImplementedError("TrashRule not implemented yet")
        if class_name == "Rename":
            NotImplementedError("RenameRule not implemented yet")
        return class_name

    @classmethod
    def instantiate_class(cls, class_name: str, attributes: Dict[str, str]) -> Rule:
        return class_name(**attributes)


class SiteParser:
    @classmethod
    def parse(
        cls, rules: List[str], path: Path or str, enabled: bool = True, **kwargs
    ) -> Site:
        if cls.checkStructure(rules, path, enabled):
            site = Site(rules=[], path=path, enabled=enabled)
            for rule in rules:
                site.rules.append(RuleParser.parseRule(rule))
            return site
        raise ValueError("Invalid config format")

    @classmethod
    def checkStructure(cls, rules: List[str], path: Path or str, enabled: bool) -> bool:
        return rules and path and enabled
