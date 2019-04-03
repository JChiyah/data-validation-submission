#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `equations` module

Author: Javier Chiyah
		Heriot-Watt University
"""


import pytest

from datavalidation.core import GeometryParameter, BikeGeometry
from datavalidation.validation.equations import get_equations, filter_equations, solve_equation, substitute_operators
from datavalidation.validation.formulae import SUBS_DICT


def test_get_equations():
	assert len(get_equations("reach")) > 0
	assert len(get_equations("stack")) > 0
	assert len(get_equations("top_tube")) > 0
	assert len(get_equations("seat_angle")) > 0

	assert len(get_equations("reach", [GeometryParameter("stack", 0), GeometryParameter("seat_angle", 0)])) == 0


def test_filter_equations():
	assert len(filter_equations(get_equations("reach"), [GeometryParameter("stack", 0), ])) == 0

	assert len(get_equations("reach",
		[GeometryParameter("top_tube", 0), GeometryParameter("stack", 0), GeometryParameter("seat_angle", 0)]
	)) > 0
	assert len(get_equations("reach",
		[GeometryParameter("top_tube", 0), GeometryParameter("stack", 0), GeometryParameter("seat_angle", "reach", 0)]
	)) > 0

	# code should not return equations when reach is part of the parameters
	assert len(get_equations("reach",
		[GeometryParameter("top_tube", 0), GeometryParameter("stack", 0), GeometryParameter("reach", 0)]
	)) == 0
	assert len(get_equations("seat_angle",
		[GeometryParameter("seat_angle", 0), GeometryParameter("stack", 0), GeometryParameter("reach", 0)]
	)) == 0


def test_solve_equation():
	test_formula = {
		"equation": "{top_tube_actual} - {stack} * TAN((90 - {seat_angle}) / 180 * PI) - {reach}",
		"parameters": [
			"reach",
			"stack",
			"seat_angle",
			"top_tube_actual"
		]
	}

	test_bike = {
		"top_tube_actual": 570,
		"stack": 595,
		"seat_angle": 73
	}

	bike = BikeGeometry.from_parameter_dict(test_bike)

	res = solve_equation(test_formula, "reach", bike)
	assert res[0] == pytest.approx(388.09, 0.1)


def test_substitute_operators():
	assert substitute_operators("PI - TAN(2)") == SUBS_DICT["PI"] + " - " + SUBS_DICT["TAN"] + "(2)"
