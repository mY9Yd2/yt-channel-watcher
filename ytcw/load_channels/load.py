import sys
from pathlib import Path

from ytcw.load_channels.from_json import from_json
from ytcw.load_channels.from_yaml import from_yaml


def load(file_path: str) -> dict[str, str]:
    file_extension = Path(file_path).suffix

    if file_extension in [".yaml", ".yml"]:
        return from_yaml(file_path)
    elif file_extension == ".json":
        return from_json(file_path)
    else:
        print(f"Not supported: {file_extension}")
        sys.exit(1)
