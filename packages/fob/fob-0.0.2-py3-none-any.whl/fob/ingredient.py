import json
import logging
import os

from functools import wraps

from .serialize import StringOutput
from .store import cacheable, parse_function_arguments
from .types import cfg_as_strings, simple_type_annotation_to_type, valid_config_types


class Ingredient:
    search_path = None
    output_path = None
    read_only = False
    artifact_log = None

    def build(self):
        if hasattr(self, "cfg"):
            for val in self.cfg.values():
                if val and isinstance(val, Ingredient):
                    val.build()

    def warm(self):
        if hasattr(self, "cfg"):
            for val in self.cfg.values():
                if val and isinstance(val, Ingredient):
                    val.warm()

    def cache_dict(self):
        cfg = {
            k: v.cache_dict() if hasattr(v, "cache_dict") else v.cache_str() if hasattr(v, "cache_str") else v
            for k, v in self.cfg.items()
        }
        return cfg

    def cache_str(self):
        if not hasattr(self, "_json_config"):
            self._json_config = json.dumps(self.cache_dict(), sort_keys=True)
        return self._json_config

    def dict_config(self):
        return {k: v.dict_config() if isinstance(v, Ingredient) else v for k, v in self.cfg.items()}

    @staticmethod
    def from_path(path, output_path=None, append_search_path=None):
        from .base import instantiate_object

        assert not path.endswith("config.json"), "pass the path to the directory, not the config.json file"
        with open(os.path.join(path, "config.json"), "rt", encoding="utf-8") as f:
            config = json.load(f)
        # LTODO is 'None' output_path the right default here, or should it be the path provided?
        # argument for None: writes are unintuitive when you run a command to "open" an ingredient you downloaded
        #   i.e., your commands are writing to a directory that you perceive to have just opened
        # argument for provided path: inexperienced/new users might be inefficient due to disabled caching
        #   (feels like a weak argument; users can learn, and may not happen in many situations, like when used as a dependency)

        search_path = [path]
        if append_search_path:
            search_path.extend(append_search_path)
        return instantiate_object(config, output_path=output_path, search_path=search_path)

    def set_paths(self, search_path, output_path, recurse=True, overwrite_existing=True):
        if overwrite_existing or not self.search_path:
            self.search_path = search_path
        if overwrite_existing or not self.output_path:
            self.output_path = output_path
        if recurse:
            for val in self.cfg.values():
                if val and isinstance(val, Ingredient):
                    val.set_paths(search_path, output_path, recurse=recurse, overwrite_existing=overwrite_existing)

    def set_artifact_logging(self, enabled=False):
        if not enabled:
            self.artifact_log = None
        if enabled and self.artifact_log is None:
            self.artifact_log = []

        for val in self.cfg.values():
            if val and isinstance(val, Ingredient):
                val.set_artifact_logging(enabled=enabled)

    def caching_like(self, obj, recurse=True):
        self.set_paths(obj.search_path, obj.output_path, recurse=recurse, overwrite_existing=True)

    def main(self):
        print("got default ingredient main for:", self)

    @cacheable(StringOutput)
    def cfg_file(self):
        return "\n".join(list(cfg_as_strings(self.cfg)))

    def print_config(self):
        lines = list(cfg_as_strings(self.cfg))
        print("\n".join(lines))

    def pretty_print_config(self):
        print("----- config -----")
        lines = []
        self._config_summary(lines)
        print("\n".join(lines))

    def _config_summary(self, lines, prefix=""):
        from colorama import Style, Fore

        # show name, followed by module config, followed by dependencies
        order = sorted(self.cfg.keys())
        for key in order:
            if key == "__name":
                continue
            if hasattr(self.cfg[key], "_config_summary"):
                lines.append(f"{prefix}{key}:{Style.RESET_ALL}")
                childprefix = prefix + "    "
                self.cfg[key]._config_summary(lines, prefix=childprefix)
            else:
                # LTODO show docstrings in help
                # if key has a description
                #     lines.append(f"{prefix}{Style.DIM}# {options[key].description}{Style.RESET_ALL}")

                color = ""
                # LTODO change color for non-default values
                # if self.cfg[key] is not its default value
                # color = Fore.GREEN
                lines.append(f"{color}{prefix}{key} = {self.cfg[key]}{Style.RESET_ALL}")

    def shell(self):
        from IPython import embed

        header = f"self.cfg: {self.cfg}\n"
        header += f"dropping into self: {type(self)}"

        embed(header=header)

    def __str__(self):
        cfgstr = json.dumps(self.cache_dict(), sort_keys=True)
        return f"Ingredient<{cfgstr}>"


def configurable(f):
    """This decorator parses __init__'s args & kwargs and stores them in a self.cfg dict.
    The keys come from the function signature, so default kwargs are present.
    """

    @wraps(f)
    def new_init(self, *args, **kwargs):
        if f.__name__ != "__init__":
            logging.getLogger(__name__).warning("@configurable decorator applied to a non-__init__ method: %s", f.__name__)
            assert not self.cfg, "would overwrite self.cfg"

        self.name = self.__module__ + "." + self.__class__.__name__
        self.cfg = {"__name": self.name}

        # populate self.cfg with the arguments passed to the function, which is typically __init__
        bound_args, _, _ = parse_function_arguments(f, [self] + list(args), kwargs)
        for k, v in bound_args.items():
            if k == "self":
                continue

            self.cfg[k] = v

            # only Ingredients and primitive types can be fully configured, so warn if any arguments cannot be
            arg_type = f.__annotations__.get(k, "missing")
            arg_type = simple_type_annotation_to_type(arg_type)[2] if arg_type != "missing" else str
            if arg_type not in valid_config_types and not issubclass(arg_type, Ingredient):
                logging.getLogger(__name__).warning("argument is not an Ingredient or primitive config type: %s", k)

        f(self, *args, **kwargs)

    return new_init
