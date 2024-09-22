import datetime
import inspect
import pathlib
from dataclasses import dataclass
from typing import Optional

from module.utils import json_load, reverse_readline


@dataclass
class FromDict:
    @classmethod
    def from_dict(cls, env: dict[str, any], field_map: dict[str, str] = None):
        out = {}
        for k, v in env.items():
            k = field_map.get(k, k) if field_map is not None else k
            if k in inspect.signature(cls).parameters:
                out[k] = v
        # noinspection PyArgumentList
        return cls(**out)


@dataclass
class FromId(FromDict):
    __fieldMap = {
        "_": "from_type",
    }
    from_type: str
    user_id: Optional[str] = None
    channel_id: Optional[int] = None

    @classmethod
    def from_dict(cls, env: dict[str, any], field_map: dict[str, str] = None):
        return super().from_dict(env, cls.__fieldMap)


@dataclass
class PeerId(FromDict):
    __fieldMap = {
        "_": "peer_type",
    }
    peer_type: str
    channel_id: int

    @classmethod
    def from_dict(cls, env: dict[str, any], field_map: dict[str, str] = None):
        return super().from_dict(env, cls.__fieldMap)


@dataclass
class ExportItem(FromDict):
    __fieldMap = {
        "from": "user",
    }
    id: int
    date: datetime.datetime
    message: str
    from_id: FromId
    actor: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    peer_id: Optional[PeerId] = None

    @classmethod
    def from_dict(cls, env: dict[str, any], field_map: dict[str, str] = None):
        return super().from_dict(env, cls.__fieldMap)


def get_user(item: ExportItem):
    return item.from_id.user_id if item.from_id is not None and hasattr(item.from_id, "user_id") else "-"


def get_items(data_path: pathlib.Path):
    for line in reverse_readline(data_path):
        data = json_load(line)

        if "message" not in data:
            continue

        data["date"] = datetime.datetime.fromisoformat(data["date"])
        data["peer_id"] = PeerId.from_dict(data.get("peer_id"))
        data["from_id"] = FromId.from_dict(data.get("from_id"))

        yield ExportItem.from_dict(data)


def test():
    t = PeerId.from_dict({"_": "PeerChannel", "channel_id": 2168150207})
    print(t)


if __name__ == "__main__":
    test()
