"""
JSON related load functions
"""

import json
from pathlib import Path

import typer


def from_json(file_path: Path) -> dict[str, list[str]]:
    """
    Deserialize JSON data from file

    Args:
        file_path (Path): Path to the file

    Returns:
        Returns a dictionary containing the loaded data

    Raises:
        typer.Exit: If the file format is not supported
    """

    try:
        return json.loads(file_path.read_text())
    except FileNotFoundError as err:
        print(err)
        raise typer.Exit(code=1)
