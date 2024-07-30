"""
This module contain the main load function
"""

from pathlib import Path

import typer

from ytcw.load_channels.from_json import from_json
from ytcw.load_channels.from_yaml import from_yaml


def load(file_path: Path) -> dict[str, list[str]]:
    """
    Load the channel identifiers from a file

    Args:
        file_path (Path): Path to the file containing the channel identifiers

    Returns:
        Returns a dictionary of categories and their channel identifiers

    Raises:
        typer.Exit: If the file format is not supported
    """

    if file_path.suffix in [".yaml", ".yml"]:
        return from_yaml(file_path)
    elif file_path.suffix == ".json":
        return from_json(file_path)
    else:
        print(f"Not supported: {file_path.suffix}")
        raise typer.Exit(code=1)
