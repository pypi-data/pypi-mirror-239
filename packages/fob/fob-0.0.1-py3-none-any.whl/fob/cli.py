import os

from collections import OrderedDict
from shlex import shlex


def parse_args(args, config_switch="--config", bool_options=["--rm"], val_options=["--output", "--search-path"]):
    before_config = []
    in_config = []
    in_option = None
    options = OrderedDict()
    found_config = False
    for arg in args:
        if arg == config_switch:
            found_config = True
            continue

        if in_option:
            options[in_option] = arg
            in_option = None
        elif arg.startswith("--"):
            if arg in val_options:
                in_option = arg
            elif arg in bool_options:
                pass
            else:
                raise ValueError("unknown option %s" % arg)
            options[arg] = ""
        elif found_config:
            in_config.append(arg)
        else:
            before_config.append(arg)

    cls, cmd = None, None
    cmd_args = []
    if len(before_config) > 0:
        cls = before_config.pop(0)
    if len(before_config) > 0:
        next_arg = before_config.pop(0)
        if "=" in next_arg:
            cmd_args.append(next_arg)
        else:
            cmd = next_arg
    cmd_args = cmd_args + before_config

    return {"options": options, "cls": cls, "cmd": cmd, "cmd_args": cmd_args, "cls_config": in_config}


######


def config_dict_to_string(d, prefix=""):
    l = []
    for k, v in d.items():
        if isinstance(v, dict):
            l.append(config_dict_to_string(v, prefix=f"{prefix}{k}."))
        else:
            l.append(f"{prefix}{k}={v}")

    return " ".join(l)


def config_string_to_dict(s):
    s = " ".join(s.split())  # remove consecutive whitespace
    return config_list_to_dict(s.split())


def config_list_to_dict(l):
    d = {}

    for k, v in _config_list_to_pairs(l):
        _dot_to_dict(d, k, v)

    return d


def _dot_to_dict(d, k, v, DEL=""):
    if k.startswith(".") or k.endswith("."):
        raise ValueError(f"invalid path: {k}")

    if "." in k:
        path = k.split(".")
        current_k = path[0]
        remaining_path = ".".join(path[1:])

        d.setdefault(current_k, {})

        _dot_to_dict(d[current_k], remaining_path, v, DEL=DEL + "  ")
    elif k.lower() == "file":
        lst = _config_file_to_list(v)
        for new_k, new_v in _config_list_to_pairs(lst):
            _dot_to_dict(d, new_k, new_v)
    else:
        d[k] = v


def _config_list_to_pairs(l):
    pairs = []
    for kv in l:
        kv = kv.strip()

        if len(kv) == 0:
            continue

        if kv.count("=") != 1:
            raise ValueError(f"invalid 'key=value' pair: {kv}")

        k, v = kv.split("=")
        if len(v) == 0:
            raise ValueError(f"invalid 'key=value' pair: {kv}")

        pairs.append((k, v))

    return pairs


def _config_file_to_list(fn):
    lst = []
    with open(os.path.expanduser(fn), "rt") as f:
        for line in f:
            lex = shlex(line)
            lex.whitespace = ""
            kvs = "".join(list(lex))
            for kv in kvs.strip().split():
                lst.append(kv)

    return lst
