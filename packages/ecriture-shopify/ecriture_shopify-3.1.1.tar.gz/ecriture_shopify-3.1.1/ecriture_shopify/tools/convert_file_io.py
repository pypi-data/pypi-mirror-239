# library
import io
from pathlib import Path


def file_to_io(path: Path) -> io.BytesIO():
    with open(path, "rb") as f:
        bytes_io = io.BytesIO(f.read())

    return bytes_io


def io_to_file(bytes_io: io.BytesIO(), path_output: Path) -> Path:
    with open(path_output, "wb") as f:
        f.write(bytes_io.getbuffer())


# end
