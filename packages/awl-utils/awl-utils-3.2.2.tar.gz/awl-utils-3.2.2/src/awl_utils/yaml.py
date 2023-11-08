import pathlib

from src.awl_utils.read_write import read_file, write_file

import yaml


def read_yaml(path: str | pathlib.Path):
    text = read_file(path)
    return yaml.load(text, Loader=yaml.Loader)


def write_yaml(path: str | pathlib.Path, data) -> pathlib.Path | None:
    text = yaml.dump(
        data,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
    )
    return write_file(path, text)
