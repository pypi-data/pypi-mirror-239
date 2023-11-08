import os.path

from yotool.config.configuer import BaseConfiguer
from yotool.util.logger import Logger


def read_config(yml_path: str) -> dict:
    if not os.path.exists(yml_path):
        raise ValueError('The configuration file in `yml_path` does not exist.')
    yml = BaseConfiguer.load(yml_path)
    return yml


def write_config(data: dict, save_path: str) -> None:
    BaseConfiguer.dump(data=data, output_path=save_path)


def try_get(config: dict, attribute: str, default: any):
    if config is not None and attribute in config and config[attribute] is not None:
        return config[attribute]
    else:
        return default


def print_config(con: dict) -> None:
    BaseConfiguer.print_config(con)
