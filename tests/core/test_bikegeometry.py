#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `bikegeometry` module

Author: Javier Chiyah
		Heriot-Watt University
"""


import pytest
from datavalidation.core import BikeGeometry


simple_json = {
	"parameter_list": [
		{
			"p": "slug",
			"v": "bike_slug_test_simple",
			"id": "random_id_simple"
		},
		{
			"p": "head_tube",
			"v": "190",
			"id": "random_id_simple"
		}
	],
	"random_id": "random_value_simple",
	"geometry_threshold": 0.5,
	"parameter_threshold": 0.6,
	"optimistic_validation": False,
	"count_calculated_params": False
}

wrong_json = {
	"parameter_list": [
		{
			"v": "bike_slug_test_wrong",
			"id": "random_id_wrong"
		},
		{
			"p": "front_centre",
			"v": "",
			"id": "random_id_wrong"
		},
		{
			"p": "head_tube",
			"v": "190",
			"id": "random_id_wrong"
		}
	],
	"random_id": "random_value_wrong"
}


def test_bike_geometry():
	bike1 = BikeGeometry(simple_json)
	assert bike1.get_parameter_value("slug") == "bike_slug_test_simple"
	assert bike1.get_parameter_value("head_tube") == 190

	bike2 = BikeGeometry(wrong_json)
	assert bike2.get_parameter("slug") is None
	assert bike2.get_parameter_value("slug") is None
	assert bike2.get_parameter_value("head_tube") == 190


def test_bike_geometry_to_json():
	bike = BikeGeometry(simple_json)
	assert bike.to_dict() == simple_json


def test_bike_geometry_parameter_list():
	bike = BikeGeometry(simple_json)
	parameters = bike.get_parameter_list()

	assert parameters
	assert all(x is not None for x in parameters)


def test_bike_get_missing_parameter_list():
	bike = BikeGeometry(wrong_json)

	assert bike._is_parameter_empty("front_centre")
	assert "front_centre" in bike.get_missing_parameter_list()
