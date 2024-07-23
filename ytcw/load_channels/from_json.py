import json
import sys


def from_json(file_path: str):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)
