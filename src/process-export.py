import argparse
import inspect
import pathlib
from dataclasses import dataclass

from module.utils import json_load
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

argparser = argparse.ArgumentParser()
argparser.add_argument("--input", "-i")
args = argparser.parse_args()


@dataclass
class FromDict:
    @classmethod
    def from_dict(cls, env: dict[str, any]):
        out = {}
        for k, v in env.items():
            if k in inspect.signature(cls).parameters:
                out[k] = v
        # noinspection PyArgumentList
        return cls(**out)


@dataclass
class ExportFromId(FromDict):
    user_id: str


@dataclass
class ExportItem(FromDict):
    date: str
    message: str
    from_id: ExportFromId


def main():
    data_path = pathlib.Path(args.input)
    data = data_path.open()

    counter = 0
    for line in data:
        data = json_load(line)
        if "message" not in data:
            continue
        from_id = data.get("from_id")
        if from_id is not None:
            user_id = from_id.get("uset_id")
            if user_id is not None:
                data["from_id"] = ExportFromId.from_dict(from_id["user_id"])

        item = ExportItem.from_dict(data)
        user = (
            item.from_id.user_id
            if item.from_id is not None and hasattr(item.from_id, "user_id")
            else "-"
        )

        counter += 1

        line = f"{counter:03} {item.date} {user} {item.message}".replace("\n", "")[:100]
        print(line)


if __name__ == "__main__":
    main()
