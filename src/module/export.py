import inspect
from dataclasses import dataclass
from typing import Optional

from module.utils import json_load


@dataclass
class FromDict:
    __fieldMap = {}

    @classmethod
    def from_dict(cls, env: dict[str, any]):
        out = {}
        for k, v in env.items():
            k = cls.__fieldMap.get(k, k)
            if k in inspect.signature(cls).parameters:
                out[k] = v
        # noinspection PyArgumentList
        return cls(**out)


@dataclass
class ExportFromId:
    user_id: str


@dataclass
class ExportItem(FromDict):
    __fieldMap = {
        "from": "from_",
    }
    id: int
    date: str
    message: str
    from_id: ExportFromId
    actor: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    from_: Optional[str] = None


def get_user(item: ExportItem):
    return (
        item.from_id.user_id
        if item.from_id is not None and hasattr(item.from_id, "user_id")
        else "-"
    )


def get_items(data_path):
    data = data_path.open()

    for line in data:
        data = json_load(line)

        if "message" not in data:
            continue
        from_id = data.get("from_id")

        if from_id is not None:
            user_id = from_id.get("user_id")
            if user_id is not None:
                data["from_id"] = ExportFromId(user_id)

        yield ExportItem.from_dict(data)
