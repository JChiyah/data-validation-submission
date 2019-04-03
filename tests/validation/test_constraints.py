#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `equations` module

Author: Javier Chiyah
		Heriot-Watt University
"""


import json

from datavalidation.core import BikeGeometry
from datavalidation.validation.constraints import filter_by_constraints, _check_constraint_list, _check_constraint, \
	_check_constraint_statistics, check_parameter_constraints


TEST_PATH = "tests/_data"

# get JSON test data
with open(TEST_PATH + "/test_geometry_1.json") as json_file:
	TEST_DATA = json.load(json_file)


def test_filter_by_constraints():
	bike = BikeGeometry.from_parameter_dict(TEST_DATA)
	value_list1 = [-100, 200]
	value_list2 = [800, 1500]

	assert filter_by_constraints(value_list1, "wheelbase", bike) == []
	assert filter_by_constraints(value_list2, "wheelbase", bike) == value_list2


def test_check_constraint_list():
	bike = BikeGeometry.from_parameter_dict(TEST_DATA)
	constraints = [
		(">", "chainstay"),
		(">", "front_centre")
	]

	assert _check_constraint_list(bike.get_parameter_value("wheelbase"), constraints, bike)


def test_check_constraint():
	bike = BikeGeometry.from_parameter_dict(TEST_DATA)

	assert _check_constraint(bike.get_parameter_value("chainstay"), ("<", "wheelbase"), bike)
	assert _check_constraint(bike.get_parameter_value("wheelbase"), (">", "chainstay"), bike)
	assert _check_constraint(bike.get_parameter_value("chainstay"), ("<=", "chainstay"), bike)
	assert _check_constraint(bike.get_parameter_value("chainstay"), (">=", "chainstay"), bike)

	# test for when the second parameter is empty or None
	bike.get_parameter("seat_tube_length")._value = 540
	bike.get_parameter("seat_tube_length_eff")._value = ""

	assert _check_constraint(bike.get_parameter_value("seat_tube_length"), ("<", "seat_tube_length_eff"), bike)

	bike.get_parameter("seat_tube_length_eff")._value = None

	assert _check_constraint(bike.get_parameter_value("seat_tube_length"), ("<", "seat_tube_length_eff"), bike)


def test_check_constraint_statistics():
	bike = BikeGeometry.from_parameter_dict(TEST_DATA)

	bike.get_parameter("chainstay")._value = 425
	bike.get_parameter("wheelbase")._value = 100
	bike.get_parameter("front_centre")._value = 600

	# the issue is in wheelbase
	assert _check_constraint_statistics("chainstay", 425, bike)
	assert _check_constraint_statistics("front_centre", 600, bike)
	assert not _check_constraint_statistics("wheelbase", 100, bike)

	bike.get_parameter("chainstay")._value = 800
	bike.get_parameter("wheelbase")._value = 1100

	# the issue is in chainstay now
	assert not _check_constraint_statistics("chainstay", 800, bike)
	assert _check_constraint_statistics("front_centre", 600, bike)
	assert _check_constraint_statistics("wheelbase", 800, bike)

	bike.get_parameter("chainstay")._value = 425
	bike.get_parameter("front_centre")._value = 5000

	# the issue is in front_centre now
	assert not _check_constraint_statistics("front_centre", 5000, bike)


def test_check_parameter_constraints():
	bike = BikeGeometry.from_parameter_dict(TEST_DATA)

	bike.get_parameter("front_centre")._value = 5000

	assert not check_parameter_constraints("front_centre", bike)
