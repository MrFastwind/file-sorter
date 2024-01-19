from pathlib import Path
from typing import Dict, Type
from ruamel.yaml import YAML
from rule.MoveRule import MoveRule, RuleFactory

from rule.Rule import Rule


class Parser:
    @classmethod
    def parseRule(cls, obj: Dict[str, str]) -> Rule:
        if not obj["type"]:
            raise ValueError("Invalid config format. Missing type")
        obj_type = obj.pop("type")
        # TODO: Implement Rules
        if obj_type == "Move":
            return MoveRule(**obj)
        if obj_type == "Delete":
            NotImplementedError("DeleteRule not implemented yet")
        if obj_type == "Keep":
            NotImplementedError("KeepRule not implemented yet")
        if obj_type == "Trash":
            NotImplementedError("TrashRule not implemented yet")
        if obj_type == "Rename":
            NotImplementedError("RenameRule not implemented yet")

        ## try to crate a class with the type name = to obj_type, and use the attributes present inside obj
        return cls.parseConfig(obj_type, obj)

    @classmethod
    def parseConfig(cls, class_name: str, attributes: Dict[str, str]) -> Rule:
        return class_name(**attributes)


class ConfigLoader:
    def __init__(self, config: Path):
        self.config = config

    def __load_config(self):
        cursor = YAML.load_all(self.config, Loader=YAML.FullLoader)
        for data in cursor:
            ...

    def get_config(self):
        return self.config
