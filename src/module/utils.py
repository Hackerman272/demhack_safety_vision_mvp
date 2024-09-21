import dataclasses
import datetime
import json
import os
import pathlib
import subprocess
from io import StringIO

from ruamel.yaml import YAML, RoundTripRepresenter


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        elif isinstance(o, pathlib.PosixPath):
            return o.as_posix()
        elif hasattr(o, "to_dict"):
            return o.to_dict()
        elif isinstance(o, bytes):
            return f"0x{o.hex()}"
        return super().default(o)


def repr_str(dumper: RoundTripRepresenter, data: str):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def repr_none(dumper: RoundTripRepresenter, _):
    return dumper.represent_scalar("tag:yaml.org,2002:null", "null")


def json_load(data: any):
    return json.loads(data)


def json_dump(data: any):
    return json.dumps(data, cls=EnhancedJSONEncoder, ensure_ascii=False)


def yaml_load(stream):
    yaml = YAML(typ="safe")
    return yaml.load_all(stream)


def yaml_dump(data: list[any]):
    yaml = YAML()
    yaml.representer.add_representer(str, repr_str)
    yaml.representer.add_representer(type(None), repr_none)

    prepared_data = json.loads(json.dumps(data, cls=EnhancedJSONEncoder))

    stream = StringIO()
    # yaml.compact(seq_seq=False, seq_map=False)
    yaml.compact()
    yaml.dump_all(prepared_data, stream)

    return stream.getvalue()


def reverse_readline(filename, buf_size=8192):
    """A generator that returns the lines of a file in reverse order"""
    with open(filename, "rb") as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            # remove file's last "\n" if it exists, only for the first buffer
            if remaining_size == file_size and buffer[-1] == ord("\n"):
                buffer = buffer[:-1]
            remaining_size -= buf_size
            lines = buffer.split("\n".encode())
            # append last chunk's segment to this chunk's last line
            if segment is not None:
                lines[-1] += segment
            segment = lines[0]
            lines = lines[1:]
            # yield lines in this chunk except the segment
            for line in reversed(lines):
                # only decode on a parsed line, to avoid utf-8 decode error
                yield line.decode()
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment.decode()


def get_pass(name: str) -> str:
    out = subprocess.run(["pass", "show", name], capture_output=True, text=True).stdout
    return str(out.rstrip("\n"))
