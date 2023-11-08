import os
from typing import Union
from collections import OrderedDict
import torch.nn as nn
import torch

from yotool.config import read_config, print_config, write_config
from yotool.util.logger import Logger


class Run:
    def __init__(self, name: str, model: nn.Module, config: Union[str, dict], output_root_path: str = 'output', **kwargs):
        assert len(name) > 0 and len(output_root_path) > 0
        self.name = name
        self.output_path = os.path.join(output_root_path, name)
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        if isinstance(config, str):
            config = read_config(config)
        config["output_path"] = self.output_path
        self.config = config
        Logger.info(f'Run \'{self.name}\'')
        Logger.info(f'Run data will be saved in \033[95m{os.path.abspath(self.output_path)}\033[0m')
        Logger.info('Run configuration:')
        print_config(self.config)

        if 'model' in self.config:
            self.model = model(self.config['model'], **kwargs)
        else:
            self.model = model(self.config, **kwargs)

    def get_model(self) -> nn.Module:
        return self.model

    def from_pretrained(self, checkpoint_path: str, mapping_handler=None) -> nn.Module:
        Logger.info(f'Load pretrianed checkpoint from \033[95m{os.path.abspath(checkpoint_path)}\033[0m')
        checkpoint = torch.load(checkpoint_path, map_location="cpu")
        if mapping_handler is not None:
            new_state_dict = OrderedDict()
            for k, v in checkpoint.items():
                key, value = mapping_handler(k, v)
                new_state_dict[key] = value
            checkpoint = new_state_dict
        self.model.load_state_dict(checkpoint)
        return self.model

    def from_config(self, checkpoint_field: str = 'checkpoint_path', mapping_handler=None) -> nn.Module:
        if checkpoint_field not in self.config:
            raise ValueError(f'Without \'{checkpoint_field}\' in configuration file,yotool cannot load checkpoint.')
        return self.from_pretrained(self.config[checkpoint_field], mapping_handler=mapping_handler)

    def save(self, config_file_name: str = 'config.yaml', checkpoint_field: str = 'checkpoint_path', checkpoint_name: str = 'checkpoint.pth') -> nn.Module:
        Logger.info(f'save run data to \033[95m{os.path.abspath(self.output_path)}\033[0m')
        self.config[checkpoint_field] = os.path.abspath(os.path.join(self.output_path, checkpoint_name))
        write_config(data=self.config, save_path=os.path.join(self.output_path, config_file_name))
        torch.save(self.model.state_dict(), os.path.join(self.output_path, checkpoint_name))
