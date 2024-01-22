import logging
from pathlib import Path
from typing import List
from attr import dataclass
from ruamel.yaml import YAML
from config.Parser import SiteParser
from config.Site import Site


@dataclass
class Config:
    sites: List[Site]


class ConfigLoader:
    def __init__(self, config: Path):
        self.config = config

    def __load_config(self):
        cursor = YAML.compose_all(self.config, Loader=YAML.FullLoader)
        self.config = Config(sites=[])
        for i, site in enumerate(cursor):
            try:
                self.config.sites.append(SiteParser.parse(site))
            except ValueError as e:
                logging.error(f"Error while loading config of site {i}: {e}")

    def get_config(self) -> Config:
        if not self.config:
            self.__load_config()
        return self.config
