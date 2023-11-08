from fob.base import instantiate_object, name_to_cls

from widget import Widget, RoundWidget


def test_name_to_cls():
    assert Widget == name_to_cls("widget.Widget")


def test_simple_instantiate_object_without_paths():
    obj = instantiate_object({"__name": "widget.RoundWidget", "radius": 2.0})
    assert obj.cfg["radius"] == 2.0
    assert obj.area() == 2 * 3 * 2.0
    assert isinstance(obj, RoundWidget)
    assert (not hasattr(obj, "search_path")) or not obj.search_path
    assert (not hasattr(obj, "output_path")) or not obj.output_path


def test_simple_instantiate_object_with_paths():
    search_path = ["/some/path"]
    obj = instantiate_object({"__name": "widget.RoundWidget", "radius": 2.0}, search_path=search_path, output_path="/output")
    assert obj.search_path == search_path
    assert obj.output_path == "/output"


def test_recursive_instantiate_object_without_paths():
    pair = instantiate_object(
        {"__name": "widget.WidgetPair", "widget1": RoundWidget(2), "widget2": {"__name": "widget.RoundWidget", "radius": 3}}
    )
    assert pair.area() == 2 * 3 * (2 + 3)


def test_recursive_instantiate_object_with_paths():
    search_path = ["/some/path"]
    pair = instantiate_object(
        {"__name": "widget.WidgetPair", "widget1": RoundWidget(2), "widget2": {"__name": "widget.RoundWidget", "radius": 3}},
        search_path=search_path,
        output_path="/output",
    )
    assert pair.search_path == search_path
    assert pair.output_path == "/output"
    # widget1 should have paths set because instantiate_object will call set_paths to replace empty ones
    assert pair.cfg["widget1"].search_path == search_path
    assert pair.cfg["widget1"].output_path == "/output"
    # widget2 should have paths set because it was created by instantiace_object
    assert pair.cfg["widget2"].search_path == search_path
    assert pair.cfg["widget2"].output_path == "/output"


def test_config_from_instantiate_object():
    pair = instantiate_object(
        {"__name": "widget.WidgetPair", "widget1": RoundWidget(2), "widget2": {"__name": "widget.RoundWidget", "radius": 3}},
    )
    assert pair.cfg["widget1"].cfg["radius"] == 2
    assert pair.cfg["widget2"].cfg["radius"] == 3

    # with default radius
    pair = instantiate_object(
        {"__name": "widget.WidgetPair", "widget1": RoundWidget(), "widget2": {"__name": "widget.RoundWidget"}},
    )
    assert pair.cfg["widget1"].cfg["radius"] == 1
    assert pair.cfg["widget2"].cfg["radius"] == 1


def test_cache_str():
    pair = instantiate_object(
        {"__name": "widget.WidgetPair", "widget1": RoundWidget(2), "widget2": {"__name": "widget.RoundWidget", "radius": 3}},
    )
    assert (
        pair.cache_str()
        == '{"__name": "widget.WidgetPair", "widget1": {"__name": "widget.RoundWidget", "radius": 2}, "widget2": {"__name": "widget.RoundWidget", "radius": 3.0}}'
    )

    pair = instantiate_object(
        {"__name": "widget.WidgetPair", "widget1": None, "widget2": {"__name": "widget.RoundWidget", "radius": 3}},
    )
    assert (
        pair.cache_str()
        == '{"__name": "widget.WidgetPair", "widget1": null, "widget2": {"__name": "widget.RoundWidget", "radius": 3.0}}'
    )
