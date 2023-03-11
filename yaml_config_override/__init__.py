import yaml
from pathlib import Path
import argparse

def __parse(config_specification, argument_root=None):
    if argument_root is None:
        argument_root = []
    for key, value in config_specification.items():
        if isinstance(value, dict):
            yield from __parse(value, argument_root + [key])
        else:
            yield '.'.join(argument_root + [key]) , value


def add_arguments(config=None):
    
    parser = argparse.ArgumentParser()

    if config is None:
        parser.add_argument("-c", "--config", type=Path)
        config = \
            yaml.safe_load(parser.parse_known_args()[0].config.read_text())

    for name, default_value in __parse(config):
        parser.add_argument('--' + name, type=type(default_value), default=default_value)

    return vars(parser.parse_args())

