from dataclasses import dataclass
import logging
from pathlib import Path
from typing import List
from ruamel.yaml import YAML
from config.Parser import SiteParser
from config.Site import Site


@dataclass
class Config:
    sites: List[Site]


class ConfigLoader:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = None

    def __load_config(self):
        cursor = YAML().load_all(self.config_path)
        self.config = Config(sites=[])
        for i, site in enumerate(next(cursor)):
            try:
                self.config.sites.append(SiteParser.parse(**site))
            except ValueError as e:
                logging.error(f"Error while loading config of site {i}: {e}")

    def get_config(self) -> Config:
        if not self.config:
            self.__load_config()
        return self.config
