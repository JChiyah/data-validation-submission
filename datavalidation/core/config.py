#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
config
----------------------------------

Module with several utility functions to configure certain parts of the package and read the config file.

The config file is located under the package's root, in `datavalidation.config`.

Author: Javier Chiyah, Heriot-Watt University, 2019
"""


import json
import logging
import pkg_resources


# name of the package that contains the config file
PACKAGE_NAME = "datavalidation"
# name of the config file
CONFIG_FILE = "config.json"

# default config if the file is corrupted or not found
DEFAULT_CONFIG = {
	"console": False,
	"level": "logging.INFO",
	"filename": "datavalidation.log",
	"filemode": "a",
	"format": "%(asctime)s [%(levelname)s]: %(message)s"
}


def read_config_file(filepath: str = CONFIG_FILE) -> dict:
	"""
	Reads the config file and returns a dict with the package config. The config file is by default under the root
	of the package "`datavalidation.config.json`".

	:param filepath: path to the config file, default is the root of the package
	:return: config dict
	"""
	config_file = DEFAULT_CONFIG
	try:
		file_string = pkg_resources.resource_string(PACKAGE_NAME, filepath)

		config_file = json.loads(file_string)
	except Exception as e:
		print("There was an error retrieving the config file of the {} package:\n{}".format(PACKAGE_NAME, e))
		print("Using default config options")

	return config_file


def set_up_logging(filepath: str = CONFIG_FILE, use_test_config: bool = False):
	"""
	Sets up the app-wide logger using the settings retrieved from the configuration file.

	Note that the `console` option was not implemented in the end.

	:param filepath: path to a custom config file, default is the package config.json file
	:param use_test_config: True to use the test configuration of the logger, default is False
	:return: None
	"""
	logging_config = read_config_file(filepath)['logging' if not use_test_config else 'logging_test']

	logging.basicConfig(
		level=eval(logging_config['level']),
		filename=logging_config['filename'],
		filemode=logging_config['filemode'],
		format=logging_config['format']
	)

	logging.debug("{} logging set up correctly".format(PACKAGE_NAME))
