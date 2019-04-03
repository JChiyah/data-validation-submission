#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
datavalidation
----------------------------------

Main module of the datavalidation package. It contains functions to validate bike geometries.

Author: Javier Chiyah and Mario Vasilev, Heriot-Watt University, 2019
"""


import logging

# from .core import BikeGeometry, set_up_logging
import datavalidation.core as dvcore
import datavalidation.core.config as dvconfig
import datavalidation.validation as validation
import datavalidation.normalisation as normalisation


# set up the logger of the whole package with the config file
dvconfig.set_up_logging()


def request_validate_bike_geometry(request_content: dict) -> dict:
	"""
	Request to validate a bike geometry.

	Example request::

		{
			"geometries": [
				{
					"geometry_threshold": 0.7,
					"parameter_threshold": 0.7,
					"parameter_list": [
						{
							"p": "reach",
							"v": "371",
							"id": "**any-value**"
						},
						{
							"p": "stack",
							"v": "533",
							"id": "**any-value**"
						}
					]
				}
			]
			# more parameters of the request ...
		}

	Check the `usage` document for more information.

	:param request_content: content of the request as a dict
	:return: request response as a dict
	"""
	logging.info("Received validate_bike_geometry request")

	request_content['geometries'] = validate_bike_geometry_list(request_content['geometries'])

	# return correctly formatted request
	logging.info("Responding to validate_bike_geometry request")
	logging.debug("Response: {}".format(request_content))

	return request_content


def validate_bike_geometry_list(bike_geometry_list: list) -> list:
	"""
	Validates a list of bike geometries.

	Example list::

		[
			# bike geometry
			{
				"parameter_list": [
					{
						"p": "reach",
						"v": "371"
					},
					{
						"p": "stack",
						"v": "533"
					}
				]
			},
			# more geometries ...
		]

	:param bike_geometry_list: list of bike geometry dicts
	:return: list of bike geometry dicts validated
	"""
	validated_geometry_list = []
	# for each bike geometry, normalise it and validate
	for geometry in bike_geometry_list:
		validated_geometry = validate_bike_geometry(geometry)

		# add it to list in dict format
		validated_geometry_list.append(validated_geometry)

	return validated_geometry_list


def validate_bike_geometry(bike_geometry_dict: dict) -> dict:
	"""
	Validates a bike geometry given a dictionary representing one.

	Example bike geometry dict::

		{
			"parameter_list": [
				{
					"p": "reach",
					"v": "371"
				},
				{
					"p": "stack",
					"v": "533"
				},
				# more bike geometry parameters ...
			]
		}

	:param bike_geometry_dict: bike geometry dict
	:return: bike geometry dict
	"""
	bike_geometry = dvcore.BikeGeometry(bike_geometry_dict)

	logging.debug("Bike geometry dump: {}".format(bike_geometry.to_dict()))

	normalisation.normalise_bike_geometry(bike_geometry)

	validation.validate_bike_geometry(bike_geometry)

	# return correctly formatted request
	bike_dict = bike_geometry.to_dict()
	logging.debug("Validated bike geometry dump: {}".format(bike_dict))

	return bike_dict
