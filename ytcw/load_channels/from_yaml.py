import sys

from omegaconf import OmegaConf


def from_yaml(file_path: str):
    try:
        return OmegaConf.load(file_path)
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)
