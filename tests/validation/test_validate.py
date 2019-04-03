#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Tests for `validation` module

Author: Javier Chiyah
		Heriot-Watt University
"""


import json
import pytest
import logging

from datavalidation.core import BikeGeometry
from datavalidation.normalisation.normalise import normalise_bike_geometry
from datavalidation.validation.validate import validate_bike_geometry, calculate_missing_parameters, get_invalid_parameters


TEST_PATH = "tests/_data"


# get JSON test data
with open(TEST_PATH + "/test_geometry_1.json") as json_file:
	TEST_DATA = json.load(json_file)


def test_validate_bike_geometry():
	bike_geo = BikeGeometry.from_parameter_dict(TEST_DATA)

	normalise_bike_geometry(bike_geo)
	validate_bike_geometry(bike_geo)

	bike_dict = bike_geo.to_dict()

	assert "confidence" in bike_dict and "invalid" in bike_dict
	assert not bike_dict['invalid']
	assert bike_dict['confidence'] > 0.7

	for parameter in bike_dict['parameter_list']:
		assert parameter['v'] is not None
		assert isinstance(parameter['v'], str)

		if "confidence" in parameter:
			assert "invalid" in parameter
			assert parameter['confidence'] > 0

	# test confidences
	optimistic = bike_geo._OPTIMISTIC_VALIDATION
	confidence1 = bike_geo.get_confidence_score()

	bike_geo._OPTIMISTIC_VALIDATION = not optimistic
	confidence2 = bike_geo.get_confidence_score()

	assert confidence1 >= confidence2 if optimistic else confidence2 >= confidence1


def test_calculate_bike_geometry():
	bike_geo = BikeGeometry.from_parameter_dict(TEST_DATA)

	normalise_bike_geometry(bike_geo)

	param_len = len(bike_geo.get_parameter_list())
	missing_len = len(bike_geo.get_missing_parameter_list())

	calculate_missing_parameters(bike_geo)

	assert param_len != len(bike_geo.get_parameter_list())
	assert missing_len != len(bike_geo.get_missing_parameter_list())


def test_validate_odd_bikes():
	bike_geo = BikeGeometry.from_parameter_dict(TEST_DATA)
	normalise_bike_geometry(bike_geo)

	bike_geo.get_parameter("wheelbase")._original_value = "100"
	bike_geo.get_parameter("wheelbase")._value = 100.0
	bike_geo.get_parameter("front_centre")._original_value = "683.09"
	bike_geo.get_parameter("front_centre")._value = 683.09

	validate_bike_geometry(bike_geo)

	# check that it calculated the wheelbase value, but confidence is low
	assert bike_geo.get_parameter("wheelbase").confidence < 0.2
	assert bike_geo.get_parameter_value("wheelbase") == pytest.approx(1100, 0.1)


def test_get_invalid_parameters():
	bike_geo = BikeGeometry.from_parameter_dict(TEST_DATA)
	normalise_bike_geometry(bike_geo)

	bike_geo.get_parameter("wheelbase")._original_value = "100"
	bike_geo.get_parameter("wheelbase")._value = 100.0
	bike_geo.get_parameter("front_centre")._original_value = ""
	bike_geo.get_parameter("front_centre")._value = None

	validate_bike_geometry(bike_geo)

	assert bike_geo.get_parameter("wheelbase").confidence < 0.2
	assert "wheelbase" in get_invalid_parameters(bike_geo)
	assert "front_centre" in bike_geo.get_missing_parameter_list()

	bike_geo.get_parameter("wheelbase")._original_value = "1011"
	bike_geo.get_parameter("wheelbase")._value = 1011.0
	bike_geo.get_parameter("wheelbase")._calculated_value = 1011.0
	bike_geo.get_parameter("front_centre")._original_value = "50000"
	bike_geo.get_parameter("front_centre")._value = 50000.0

	validate_bike_geometry(bike_geo)

	assert "front_centre" in get_invalid_parameters(bike_geo)
	assert "front_centre" not in bike_geo.get_missing_parameter_list()

	assert bike_geo.get_parameter("front_centre").confidence < 0.2
	assert bike_geo.get_parameter_value("front_centre") == pytest.approx(594.56, 0.1)


def test_validate_calculated_parameters():
	logging.info("test_validate_calculated_parameters")
	bike_geo = BikeGeometry.from_parameter_dict(TEST_DATA)
	normalise_bike_geometry(bike_geo)

	validate_bike_geometry(bike_geo)

	previous_reach = bike_geo.get_parameter_value("reach")
	previous_stack = bike_geo.get_parameter_value("stack")
	previous_head_angle = bike_geo.get_parameter_value("head_angle")

	# reach
	bike_geo.get_parameter("reach")._original_value = "7000"
	bike_geo.get_parameter("reach")._value = 7000.0
	bike_geo.get_parameter("reach")._calculated_value = None
	bike_geo.get_parameter("reach")._confidence = None

	validate_bike_geometry(bike_geo)

	reach_param = bike_geo.get_parameter("reach")
	assert reach_param.confidence < 0.3
	assert reach_param.calculated_value == pytest.approx(previous_reach, 5)

	# stack
	bike_geo.get_parameter("stack")._original_value = "7000"
	bike_geo.get_parameter("stack")._value = 7000.0
	bike_geo.get_parameter("stack")._calculated_value = None
	bike_geo.get_parameter("stack")._confidence = None

	validate_bike_geometry(bike_geo)

	stack_param = bike_geo.get_parameter("stack")
	assert stack_param.confidence < 0.3
	assert stack_param.calculated_value == pytest.approx(previous_stack, 5)

	# head_angle
	bike_geo.get_parameter("head_angle")._original_value = "260"
	bike_geo.get_parameter("head_angle")._value = 260.0
	bike_geo.get_parameter("head_angle")._calculated_value = None
	bike_geo.get_parameter("head_angle")._confidence = None

	validate_bike_geometry(bike_geo)

	head_angle_param = bike_geo.get_parameter("head_angle")
	assert head_angle_param.confidence < 0.5
	assert head_angle_param.calculated_value == pytest.approx(previous_head_angle, 0.1)
