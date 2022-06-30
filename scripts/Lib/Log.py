# coding=utf-8

import os
import platform
import logging


def get_username():
	if platform.system() == "Windows":
		name = os.getenv("USERNAME")
	return name


class MaterialStatusLog:
	def __init__(self, name):
		self._name = name
		self._logger = logging.getLogger()
		self._logger.name = get_username()
		self._stream_handler = logging.StreamHandler()

	def initialzie_log(self):
		formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
		self._stream_handler.setFormatter(formatter)
		self._logger.addHandler(self._stream_handler)

	def message(self, val):
		logging.info(val)

	def exception(self, err_type, val):
		logging.exception("{0} - {1}:{2}".format(self._name, err_type, val))

	def error(self, stop_point, val):
		logging.error("{0} - {1}:{2}".format(self._name, stop_point, val))

	def critical(self, stop_point, val):
		logging.critical("{0} - {1}:{2}".format(self._name, stop_point, val))