import pathlib
from typing import Any

from mergedeep import merge
from module.utils import yaml_load


class Config(object):
    def to_dict(self):
        out = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Config):
                out[key] = value.to_dict()
            elif not key.startswith("_"):
                out[key] = value
        return out

    def keys(self):
        return self.to_dict().keys()

    def items(self):
        return self.to_dict().items()

    def __getattribute__(self, name):
        obj = object.__getattribute__(self, name)
        if name.startswith("__") and name.endswith("__"):
            return obj
        return obj


def to_config(obj, conf: dict):
    for key, value in conf.items():
        if isinstance(value, dict):
            _obj = Config()
            setattr(obj, key, _obj)
            to_config(_obj, value)
        else:
            setattr(obj, key, value)


def get_config(config_files: list[pathlib.Path], root_dir: pathlib.Path | None = None):
    config = Config()

    merged_config: Any = {}
    for file_path in config_files:
        if file_path.exists():
            merged_config = merge(merged_config, next(yaml_load(file_path.open())))

    if root_dir is not None:
        merged_config["root_dir"] = root_dir

    to_config(config, merged_config)

    return config
