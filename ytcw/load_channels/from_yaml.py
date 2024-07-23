from pathlib import Path

import strictyaml
import typer


def from_yaml(file_path: Path) -> dict[str, list[str]]:
    try:
        return strictyaml.load(file_path.read_text()).data
    except FileNotFoundError as err:
        print(err)
        raise typer.Exit(code=1)
