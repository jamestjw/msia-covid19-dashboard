import sys
import yaml


def load_config():
    try:
        with open("config.yml", "r") as f:
            # TODO: Ensure that the config file has the required info
            return yaml.load(f.read(), Loader=yaml.FullLoader)
    except Exception as e:
        print(f"Unable to read or parse config file: {e}", file=sys.stderr)
        sys.exit(1)
