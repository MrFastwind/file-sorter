from Manager import Manager
from pathlib import Path
import argparse

from config.Config import ConfigLoader


def writeDefaultConfig(path: Path):
    path.write_text(
        """
        [
            {
                path: "{path}",
                enabled: false
                rules: [
                    {type: "Keep",
                    filter: "**/*.*"
                    }
                ]
            }
        ]
        """.format(
            path=Path.home() / "Downloads/"
        )
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

    manager = Manager()
    # run Manager
    ...


if __name__ == "__main__":
    main()
