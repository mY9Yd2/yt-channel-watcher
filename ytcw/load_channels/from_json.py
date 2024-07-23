import json
from pathlib import Path

import typer


def from_json(file_path: Path) -> dict[str, list[str]]:
    try:
        return json.loads(file_path.read_text())
    except FileNotFoundError as err:
        print(err)
        raise typer.Exit(code=1)
