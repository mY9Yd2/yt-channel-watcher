"""
YAML related load functions
"""

from pathlib import Path

import strictyaml
import typer


def from_yaml(file_path: Path) -> dict[str, list[str]]:
    """
    Deserialize YAML data from file

    Args:
        file_path (Path): Path to the file

    Returns:
        Returns a dictionary containing the loaded data

    Raises:
        typer.Exit: If the file format is not supported
    """

    try:
        return strictyaml.load(file_path.read_text()).data
    except FileNotFoundError as err:
        print(err)
        raise typer.Exit(code=1)
