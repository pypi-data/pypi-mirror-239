import os

import pytest

from fob.cli import parse_args, config_list_to_dict, config_string_to_dict, config_dict_to_string


def test_parse_args():
    examples = {
        "task.foo eps=42 --output bar --rm": {
            "cls": "task.foo",
            "cmd": None,
            "cmd_args": ["eps=42"],
            "options": {"--rm": "", "--output": "bar"},
            "cls_config": [],
        },
        "task.rerank.Rerank benchmark.collection.stats ca=SomeArg --get-path --search-path foo --config benchmark.collection.name=foo benchmark.thing=xyz": {
            "cls": "task.rerank.Rerank",
            "cmd": "benchmark.collection.stats",
            "cmd_args": ["ca=SomeArg"],
            "options": {"--get-path": "", "--search-path": "foo"},
            "cls_config": ["benchmark.collection.name=foo", "benchmark.thing=xyz"],
        },
    }

    for argstr, d in examples.items():
        assert parse_args(argstr.split(), bool_options=["--get-path", "--rm"]) == d

    with pytest.raises(ValueError):
        parse_args(["--bad-option"])


def test_config_list_to_dict():
    args = ["foo.bar=yes", " ", "main=42", "  \n "]
    assert config_list_to_dict(args) == {"foo": {"bar": "yes"}, "main": "42"}

    args = ["foo.bar=yes", "main=42", "foo.bar=override"]
    assert config_list_to_dict(args) == {"foo": {"bar": "override"}, "main": "42"}

    for invalid in ["inv", ".inv", "inv.", "inv=", "inv.=1", ".inv=1"]:
        args = [invalid]
        with pytest.raises(ValueError):
            config_list_to_dict(args)


def test_config_string_to_dict():
    s = "foo.bar=yes   main=42  \n  "
    assert config_string_to_dict(s) == {"foo": {"bar": "yes"}, "main": "42"}


def test_config_string_with_files_to_dict(tmpdir):
    mainfn = os.path.join(tmpdir, "main.txt")
    with open(mainfn, "wt") as f:
        print("main=24  # comment", file=f)
        print("#main=25", file=f)

    foofn = os.path.join(tmpdir, "foo.txt")
    with open(foofn, "wt") as f:
        print("test1=20  submod1.test1=21 ", file=f)
        print("submod1.submod2.test1=22", file=f)
        print("test3=extra", file=f)
        print(f"FILE={mainfn}", file=f)

    args = ["foo.test1=1", f"foo.file={foofn}", "main=42", f"file={mainfn}"]
    assert config_list_to_dict(args) == {
        "foo": {"test1": "20", "test3": "extra", "main": "24", "submod1": {"test1": "21", "submod2": {"test1": "22"}}},
        "main": "24",
    }


def test_simple_config_dict_to_string():
    d = {"foo": 1, "__name": "bar"}
    dset = set(config_dict_to_string(d).split(" "))
    assert len(dset) == 2
    assert "foo=1" in dset
    assert "__name=bar" in dset


def test_nested_config_dict_to_string():
    thing1 = {"__name": "thing1", "val": 123}
    thing2 = {"__name": "thingparent", "child": {"val": 1, "grandchild": {"val": 0}}}
    d = {"foo": 1, "__name": "bar", "thing1": thing1, "thing2": thing2}
    dset = set(config_dict_to_string(d).split(" "))
    assert len(dset) == 7
    assert "foo=1" in dset
    assert "__name=bar" in dset
    assert "thing1.__name=thing1" in dset
    assert "thing1.val=123" in dset
    assert "thing2.__name=thingparent" in dset
    assert "thing2.child.val=1" in dset
    assert "thing2.child.grandchild.val=0" in dset
