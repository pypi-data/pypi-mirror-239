import importlib
import inspect
import logging
import pickle
import sys

from fob.cli import config_list_to_dict, parse_args
from fob.ingredient import Ingredient
from fob.store import parse_function_arguments, ReadOnlyException
from fob.types import cast_dict_to_types


logger = logging.getLogger(__name__)


def name_to_cls(name):
    path = name.split(".")
    mod_str = ".".join(path[:-1])
    cls_str = path[-1]

    mod = importlib.import_module(mod_str)
    cls = getattr(mod, cls_str)
    return cls


def instantiate_object(config, search_path=None, output_path=None):
    assert "__name" in config
    assert all(isinstance(k, str) for k in config)
    assert all(isinstance(v, (str, float, int, bool, dict, list, tuple, type(None), Ingredient)) for v in config.values())

    cls = name_to_cls(config["__name"])
    logger.debug("instantiate_object %s with config: %s", cls, config)

    # cast types to those in the type annotation
    config = cast_dict_to_types(config, cls.__init__.__annotations__)

    # add default args into config, so that it describes exactly what is instantiated
    default_args = {k: v.default for k, v in inspect.signature(cls).parameters.items() if k != "self"}
    for k, v in default_args.items():
        if k not in config:
            config[k] = v

    # create the final config, which serves as kwargs, by calling instantiate_object to create any ingredients requested
    # first, separate the config keys corresponding to ingredients (dep_keys) from those that are primitives (string, int, etc)
    newcfg = {k: v for k, v in config.items() if not isinstance(v, dict) and not isinstance(v, Ingredient)}
    dep_keys = [k for k in config if k not in newcfg]

    # next, add the ingredients back into newcfg, handling the (1) Ingredient object and (2) config dict cases
    for k in dep_keys:
        if isinstance(config[k], Ingredient):
            # (1) we have an Ingredient object, so copy it over directly and set its cache paths
            newcfg[k] = config[k]
            # if either of the Ingredient's paths are None, set_paths will replace them with the path given to instantiate_object.
            # without this, default args like index=AnseriniIndex() will raise errors due to having output_path=None.
            config[k].set_paths(search_path=search_path, output_path=output_path, recurse=True, overwrite_existing=False)
        else:
            # (2) we have a config dict for an Ingredient, so use instantiate_object to create it
            newcfg[k] = instantiate_object(config[k].copy(), search_path=search_path, output_path=output_path)

    # finally, use newcfg as kwargs and instantiate cls
    kwargs = {k: v for k, v in newcfg.items() if k != "__name"}
    obj = cls(**kwargs)
    obj.search_path = search_path
    obj.output_path = output_path
    return obj


def __main__():
    if len(sys.argv) < 2:
        print("usage: <class> [method] [--output DIR] [--config ... key=val ... foo=bar ...]")
        sys.exit(1)

    args = parse_args(
        sys.argv[1:], bool_options=["--rm", "--get-path", "--log-artifacts"], val_options=["--output", "--search-path"]
    )
    logger.debug("parsed arguments: %s", args)

    config = config_list_to_dict(args["cls_config"])
    config["__name"] = args["cls"]
    cmd = args["cmd"] if args["cmd"] else "main"
    cmd_args = config_list_to_dict(args["cmd_args"])

    output_path = args["options"].get("--output", "/doesnt/exist")
    search_path = args["options"]["--search-path"].split(":") if "--search-path" in args["options"] else []
    if output_path not in search_path:
        search_path.append(output_path)

    obj = instantiate_object(config, search_path=search_path, output_path=output_path)

    # cmd is an ingredient path followed by a method, like index.collection.somemethod
    # find the method and replace obj with the index.collection
    cmd_parts = cmd.split(".")
    methodstr = cmd_parts.pop()
    for ingredient in cmd_parts:
        obj = obj.cfg[ingredient]

    method = getattr(obj, methodstr)

    if "--log-artifacts" in args["options"]:
        if hasattr(obj, "set_artifact_logging"):
            obj.set_artifact_logging(enabled=True)
        else:
            logger.warning("cannot --log-artifacts because %s has no set_artifact_logging method", obj)

    if "from_pkl" in cmd_args:
        with open(cmd_args["from_pkl"], "rb") as f:
            cmd_args = pickle.load(f)
    else:
        _, invalid_args, default_args = parse_function_arguments(method, args=[], kwargs=cmd_args)
        if invalid_args:
            raise RuntimeError(
                f"invalid arguments for method command {methodstr}: {invalid_args.keys()}"
                + f"\n\tThis method's default arguments are: {default_args}"
            )

        cmd_args = cast_dict_to_types(cmd_args, method.__annotations__)

    # handle --rm by removing the cached output, if it exists
    if "--rm" in args["options"]:
        obj.build()
        try:
            output = method(_read_only=True, _output_tuple=True, **cmd_args)
        except ReadOnlyException:
            output = None

        if output:
            output.rm()
            print("removed:", output.path)
        return

    # need a tuple so we can read the path later
    if "--get-path" in args["options"]:
        cmd_args["_output_tuple"] = True

    obj.build()
    output = method(**cmd_args)

    if "--get-path" in args["options"]:
        print("path:", output.path)

    if "--log-artifacts" in args["options"]:
        print("-------------- artifact log records ----------------")

        def gather_logs(o, log):
            if o.artifact_log:
                log.extend(o.artifact_log)
            for dep in o.cfg.values():
                if hasattr(dep, "artifact_log"):
                    gather_logs(dep, log)

        log = []
        gather_logs(obj, log)
        for entry in log:
            print(
                f"cache={entry.output.from_cache} duration={entry.end_time-entry.start_time}"
                + f"\tstart={entry.start_time}\tend={entry.end_time}"
            )
            print("\t" + " ".join(entry.cmd))
        # with open("artlogs.pkl", "wb") as outf:
        #     pickle.dump(log, outf)

    # print("\ncommand output:", output)
    return output

    # consider:
    # --cp: copy the final output object to the given path (this might be empty...)
    # output.cp(dest)
    # --mv: move the final output object to the given path (this might be empty...)
    # output.mv(dest)
    # a 'cls' version of the above, like --cls-cp and --cls-rm, that operate on all artifacts for the cls (with the current cfg)
    #                                 or --cp-cls


if __name__ == "__main__":
    __main__()
