import pathlib


def read_file(path: str | pathlib.Path) -> str:
    path = pathlib.Path(path)

    try:
        with open(path.resolve().as_posix()) as f:
            data = f.read()
    except (Exception,):
        print('Error with read ... ')
        return

    return data


def write_file(path: str | pathlib.Path, data, mode='w+') -> pathlib.Path | None:
    path = pathlib.Path(path)
    try:
        with open(path.resolve().as_posix(), mode) as f:
            f.write(data)
    except (Exception,):
        print('Error with write .... ')
        return

    return path
