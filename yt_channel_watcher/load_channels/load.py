import os
import sys

from load_channels.from_json import from_json
from load_channels.from_yaml import from_yaml


def load(file_path: str) -> dict[str, str]:
    _, file_extension = os.path.splitext(file_path)

    if file_extension in [".yaml", ".yml"]:
        return from_yaml(file_path)
    elif file_extension == ".json":
        return from_json(file_path)
    else:
        print(f"Not supported: {file_extension}")
        sys.exit(1)
