import logging
from Manager import FolderManager
from pathlib import Path
import argparse
from action.ActionInvoker import ActionInvoker, ExecutionerActionInvoker

from config.Config import ConfigLoader


def writeDefaultConfig(path: Path):
    logging.info(msg="Creating default config")
    logging.debug(msg=f"Config path: {path}")
    logging.debug(msg=f"Home path: {Path.home() / 'Downloads/'}")
    path.write_text(
        """
        [
            {
        """
        + '    path: "{0}",'.format(
            str(Path.home() / "Downloads/").replace("\\", "\\\\")
        )
        + """
                enabled: false,
                rules: [
                    {type: "Keep",
                    filter: "**/*.*"
                    }
                ]
            }
        ]
        """
    )


def getDefaultFile():
    homeconfig = Path.home() / ".filesorter.yml"

    if not homeconfig.exists():
        writeDefaultConfig(homeconfig)

    return homeconfig


def main():
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument("-c", "--config", help="Path to the config file")
    args = parser.parse_args()

    config_file = args.config if args.config else getDefaultFile()
    config = ConfigLoader(config_file).get_config()

    reports = []

    logging.info("Starting FileSorter")

    invoker: ActionInvoker = ExecutionerActionInvoker()

    for site in config.sites:
        manager = FolderManager()
        manager.setFolder(Path(site.path))
        manager.setRules(site.rules)
        manager.setInvoker(invoker)
        manager.run()
    invoker.close()
    logging.info("Finished FileSorter. Reports: %s", invoker.report())


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()
