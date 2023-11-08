import os.path

import os
from collections import OrderedDict
import yaml

from yotool.util.logger import Logger

represent_dict_order = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
yaml.add_representer(OrderedDict, represent_dict_order)


class BaseConfiguer:
    MAX_LENGTH = 30

    def __init__(self):
        pass

    @classmethod
    def load(cls, file_path: str):
        if '.yaml' not in file_path and '.yml' not in file_path:
            raise ValueError('The value of `file_path` should be a path to a yaml file.')
        root_path = os.path.dirname(os.path.abspath(file_path))

        def get_yaml_data(path: str):
            with open(path, encoding='utf-8') as file:
                return yaml.safe_load(file.read())

        def overwrite(ori: dict, con: dict) -> dict:
            _con = OrderedDict()
            _con.update(con)
            for k, v in ori.items():
                if isinstance(v, dict) and k in _con:
                    _con[k] = overwrite(ori[k], _con[k])
                else:
                    _con[k] = v
            return _con

        _origin = get_yaml_data(file_path)
        _config = OrderedDict()
        if 'inherit' in _origin:
            if isinstance(_origin['inherit'], str):
                inherit_path = _origin['inherit'] if os.path.isabs(_origin['inherit']) else os.path.join(root_path, _origin['inherit'])
                _config.update(cls.load(inherit_path))
            else:
                raise TypeError(f'The field of `inherit` in "{os.path.abspath(file_path)}` should be a string.')
        for key, value in _origin.items():
            if key not in 'inherit':
                if isinstance(value, dict) and key in _config:
                    _config[key] = overwrite(_origin[key], _config[key])
                else:
                    _config[key] = value
        return _config

    @classmethod
    def dump(cls, data: any, output_path: str):
        with open(output_path, "w", encoding='utf-8') as fo:
            yaml.dump(data, fo, default_flow_style=False)

    def handleOvergLength(self, sentence: str) -> dict:
        sentence = sentence if len(sentence) < self.MAX_LENGTH else sentence[:self.MAX_LENGTH - 1 - 3] + '...'
        return sentence

    @classmethod
    def print_config(cls, con: dict) -> None:
        max_length = 0
        for key, value in con.items():
            value = str(value)
            max_length = max(len(key), len(value), 20, max_length)
        max_length = min(max_length, cls.MAX_LENGTH)
        for key, value in con.items():
            Logger.info(cls.handleOvergLength(cls,key).rjust(max_length) + ' = ' + cls.handleOvergLength(cls,str(value)))
