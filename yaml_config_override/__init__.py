import yaml
from pathlib import Path
import argparse
import copy

def __parse(config_specification, argument_root=None):
    if argument_root is None:
        argument_root = []
    for key, value in config_specification.items():
        if isinstance(value, dict):
            yield from __parse(value, argument_root + [key])
        else:
            yield '.'.join(argument_root + [key]) , value

def __update_config(config, keys, value):
    if len(keys) == 1:
        config.setdefault(keys[0], value)
    else:    
        config.setdefault(keys[0], {})
        config[keys[0]] = __update_config(config[keys[0]], keys[1:], value)

    return config

def add_arguments(config=None):
    
    parser = argparse.ArgumentParser()

    if config is None:
        parser.add_argument("-c", "--config", type=Path)
        config = \
            yaml.safe_load(parser.parse_known_args()[0].config.read_text())

    for name, default_value in __parse(config):
        parser.add_argument('--' + name, type=type(default_value), default=default_value)

    config_parsed = {}
    for key, value in vars(parser.parse_known_args()[0]).items():
        if key == 'config':
            continue

        keys = key.split('.')
        config_parsed = __update_config(config_parsed, keys, value)
        
    return config_parsed

