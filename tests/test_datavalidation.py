#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_datavalidation
----------------------------------

Tests for `datavalidation` module.
"""


import json
import logging

from datavalidation.core.config import set_up_logging

# set logging before importing datavalidation to override test file
set_up_logging(use_test_config=True)


from datavalidation import datavalidation


TEST_PATH = "tests/_data"


# get JSON test data
with open(TEST_PATH + "/test_request_1.json") as json_file:
	TEST_DATA = json.load(json_file)

with open(TEST_PATH + "/test_request_wrong.json") as json_file:
	TEST_WRONG_DATA = json.load(json_file)


def test_datavalidation():
	logging.info("test_datavalidation")
	response = datavalidation.request_validate_bike_geometry(TEST_DATA)

	assert "confidence" in response['geometries'][0] and "invalid" in response['geometries'][0]


def test_datavalidation_wrong():
	# try with stupid and/or missing values for the parameters at the same time
	response = datavalidation.request_validate_bike_geometry(TEST_WRONG_DATA)

	assert "confidence" in response['geometries'][0] and "invalid" in response['geometries'][0]
	assert response['geometries'][0]['confidence'] < 0.7 and response['geometries'][0]['invalid']
