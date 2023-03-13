import copy
import yaml
from pathlib import Path
import argparse


def call_dict(diction, args):
    args_list = args.split(".")
    for arg in args_list:
        diction = diction[arg]
    return diction


def update(diction, path, val):
    if len(path) > 1:
        update(diction[path[0]], path[1:], val)
    else:
        diction[path[0]] = val
        return None


def add_arguments(conf1=None):
    parser = argparse.ArgumentParser()
    if conf1 is None:
        parser.add_argument("-c", "--config", type=Path)
        args = vars(parser.parse_known_args()[0])
        conf = yaml.safe_load(args["config"].read_text())
    else:
        conf = copy.deepcopy(conf1)
    args_to_create = {}
    dfs = []
    visited = set()
    root = list(conf.keys())
    dfs = dfs + [str(x) for x in root]
    while len(dfs) > 0:
        cur = dfs.pop()
        if cur in visited:
            continue
        visited.add(cur)
        cur_call = call_dict(conf, cur)
        if isinstance(call_dict(conf, cur), dict):
            dfs = dfs + [str(cur) + "." + str(x) for x in list(cur_call.keys())]
        else:
            args_to_create["--" + str(cur)] = type(cur_call)

    for key, val in args_to_create.items():
        parser.add_argument(key, type=val, required=False)
    args = vars(parser.parse_args())
    for key, val in args_to_create.items():
        ckey = key[2:]
        if args[ckey] is not None:
            _list = ckey.split(".")
            update(conf, _list, args[ckey])
    return conf

