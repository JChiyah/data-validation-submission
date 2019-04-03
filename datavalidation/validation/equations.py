#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
equations
----------------------------------

Module containing functions that get and solve equations for a given GeometryParameter.

Author: Javier Chiyah, Heriot-Watt University, 2019
"""


import re
import sympy
import sympy.solvers
import logging

from datavalidation.core import BikeGeometry
from .constraints import filter_by_constraints
from .formulae import VALIDATION_FORMULAE, SUBS_DICT


# this can be anything, but x looks good when solving equations
UNKNOWN_PARAMETER = "x"


def get_equations(parameter_name: str, filter_by: list = None) -> list:
	"""
	Gets a list of equations for the given GeometryParameter name. If a list of parameters is given as the filter,
	it will return only those equations that can be calculated using that list.
	For instance, if to calculate chainstay we need wheelbase and bb_drop, it will return the equation if the filter_by
	list contains both the wheelbase and the bb_drop.

	:param parameter_name: name of the GeometryParameter
	:param filter_by: list of GeometryParameters available that are not empty
	:return: list of equations, [] if none could be found
	"""
	result_list = []

	regex = re.compile(r'{' + parameter_name + '}')
	for formula in VALIDATION_FORMULAE:
		if parameter_name in formula['parameters'] and len(regex.findall(formula['equation'])) == 1:
			result_list.append(formula)

	if filter_by is not None:
		return filter_equations(result_list, filter_by, parameter_name)

	return result_list


def filter_equations(equation_list: list, filter_by: list = None, parameter_name: str = None) -> list:
	"""
	Filters a list of equations depending on a list of the GeometryParameters available.

	:param equation_list: list of equations
	:param filter_by: list of available GeometryParameters that are not empty
	:param parameter_name: name of the parameter that you want to use (if known)
	:return: list of filtered equations, [] if none left after filtering
	"""
	if len(equation_list) == 0 or len(filter_by) == 0:
		return equation_list

	# get only the parameter names of the list of GeometryParameters
	reduced_list = [x.name for x in filter_by if x.value is not None]

	if parameter_name is not None:
		reduced_list = [x for x in reduced_list if x != parameter_name]

	result_list = []

	for equation in equation_list:
		# count params of equation in the reduced list
		params = sum(el in equation['parameters'] for el in reduced_list)

		if params >= len(equation['parameters']) - 1:
			result_list.append(equation)

	return result_list


def solve_equation(formula, symbol_to_solve: str, bike_geometry: BikeGeometry, force_constraints: bool = True) -> list:
	"""
	Solves an equation and returns the possible solutions. This is the main function used to calculate parameter values.
	Equations with square roots return multiple solutions, increasing exponentially with additional square roots in
	the equation.

	Examples::

		>> formula = {
			"equation": "SQRT({bb_drop}^2 + ({wheelbase} - SQRT( {front_centre}^2 - {bb_drop}^2 ))^2 ) - {chainstay}",
			"parameters": [ "bb_drop", "chainstay", "wheelbase", "front_centre" ]
		}
		# get all solutions
		>> solve_equation(formula, "chainstay", bike_geometry, force_constraints=False)
		[-200, 500, 1500]
		# get solutions filtered by constraints
		>> solve_equation(formula, "chainstay", bike_geometry, force_constraints=True)
		[500]


	It is safe to use in parallel as it only reads values, it does not modify anything inside the BikeGeometry or its
	GeometryParameters.

	:param formula: a formula dict with an equation
	:param symbol_to_solve: name of the GeometryParameter to solve the equation for
	:param bike_geometry: the BikeGeometry
	:param force_constraints: if the solutions returned should enforce geometry constraints, True by default
	:return: list of possible solutions, [] if no solutions found
	"""
	equation = substitute_operators(formula['equation'])

	# replace parameters and the symbol_to_solve by x
	equation = substitute_parameters(equation, formula['parameters'], symbol_to_solve, bike_geometry)

	x = sympy.Symbol(UNKNOWN_PARAMETER, positive=True)

	# logging.debug("Solving for " + symbol_to_solve)
	# logging.debug(equation)

	try:
		# although the following statements have been thoroughly tested and they do not crash,
		# they are in a try/catch block to avoid any issues in production. The package sympy sometimes has
		# unexpected execution and raises an exception if there was an error with the formula
		# (it's due to the way that equations are solved in sympy, as expanding certain equations with some values
		# make them unsolvable).
		expr = eval(equation)
		results = sympy.solvers.solve(expr, x, domain=sympy.S.Reals)
	except Exception as e:
		logging.error("There was an error solving the following equation for '{}': \n{}\n{}".format(
			symbol_to_solve, equation, e))
		results = []

	# logging.debug("   = " + str(results))

	if force_constraints:
		results = filter_by_constraints(results, symbol_to_solve, bike_geometry)

	return results


def substitute_operators(equation):
	"""
	Substitutes the operators in an equation (e.g. TAN for sympy.tan).
	It accepts both an equation as a string or a list of equation strings.

	:param equation: equation as a string or a list
	:return: equation as a string or a list
	"""
	if isinstance(equation, list):
		return [substitute_operators(x) for x in equation]

	else:
		result = equation

		for key, val in SUBS_DICT.items():
			result = result.replace(key, val)

		return result


def substitute_parameters(equation, parameter_list: list, symbol_to_solve: str, bike_geometry: BikeGeometry):
	"""
	Substitutes the GeometryParameters of an equation using the values from the BikeGeometry. In other words,
	it substitutes the variables like {bb_drop} by their actual numeric value in the equation.

	:param equation: equation as a string or a list
	:param parameter_list: list of parameters of the equation
	:param symbol_to_solve: GeometryParameter name to solve the equation for (aka the X)
	:param bike_geometry: the BikeGeometry
	:return: equation as a string or a list
	"""
	if isinstance(equation, list):
		return [substitute_parameters(x, parameter_list, symbol_to_solve, bike_geometry) for x in equation]

	else:
		equation = equation.replace("{" + symbol_to_solve + "}", UNKNOWN_PARAMETER)

		# substitute parameters
		for param in parameter_list:
			bike_p = bike_geometry.get_parameter_value(param)
			equation = equation.replace("{" + param + "}", str(bike_p) if not isinstance(bike_p, list) else str(bike_p[0]))

		return equation
