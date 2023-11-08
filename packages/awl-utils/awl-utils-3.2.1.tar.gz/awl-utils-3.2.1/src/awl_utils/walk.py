import os
import pathlib


def walk_files(path: str | pathlib.Path) -> list[pathlib.Path]:
    path = pathlib.Path(path)
    data = []
    for root, dirs, files in os.walk(path.as_posix(), topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            data.append(file_path)

    all_files = [pathlib.Path(file) for file in data]
    return all_files
