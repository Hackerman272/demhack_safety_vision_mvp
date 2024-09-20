# version: 0.2.0

import dataclasses
import datetime
import json
import pathlib
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
    return json.dumps(data, cls=EnhancedJSONEncoder)


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
