import pytest
from project import calculate_drawer_front_dimensions, calculate_needed_parts, create_build_plan


def test_get_cabinet_version(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "d")
    output = input("What kind of cabinet do you want to build:\ns) Cabinet with shelves\nd) Cabinet with drawers\nChoice: ").lower()
    assert output == "d"


def test_calculate_drawer_front_dimensions():
    width = 500
    height = 500
    number_of_components = 2
    output = calculate_drawer_front_dimensions(width, height, number_of_components)
    assert output == (468, 231)


def test_calculate_needed_parts():
    width = 500
    depth = 100
    height = 500
    cabinet_version = "d"
    number_of_components = 2
    drawer_width = 50
    drawer_height = 20
    output = calculate_needed_parts(width, depth, height, cabinet_version, number_of_components, drawer_width, drawer_height)
    assert output == {'back_amount': 1, 'back_height': 500, 'back_thickness': 12, 'back_width': 500, 'bottom_and_top_amount': 2, 'bottom_and_top_height': 500, 'bottom_and_top_thickness': 15, 'bottom_and_top_width': 88, 'drawer_bottoms_amount': 2, 'drawer_bottoms_height': 44, 'drawer_bottoms_thickness': 15, 'drawer_bottoms_width': 414, 'drawer_frontpanels_amount': 2, 'drawer_frontpanels_height': 20, 'drawer_frontpanels_thickness': 12, 'drawer_frontpanels_width': 50, 'drawer_fronts_and_backs_amount': 4, 'drawer_fronts_and_backs_height': 100, 'drawer_fronts_and_backs_thickness': 15, 'drawer_fronts_and_backs_width': 414, 'drawer_sides_amount': 4, 'drawer_sides_height': 100, 'drawer_sides_thickness': 15, 'drawer_sides_width': 74, 'sides_amount': 2, 'sides_height': 470, 'sides_thickness': 15, 'sides_width': 88}
