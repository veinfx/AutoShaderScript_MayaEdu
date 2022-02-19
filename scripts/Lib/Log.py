# coding=utf-8

import logging


class MaterialStatusLog:
	def __init__(self):
		self._logger = logging.getLogger()
		self._stream_handler = logging.StreamHandler()

	def initialzie_log(self):
		formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
		self._stream_handler.setFormatter(formatter)
		self._logger.addHandler(self._stream_handler)

	def message(self, val):
		logging.info(val)

	def exception(self, err_type, val):
		logging.exception("{}:{}".format(err_type, val))

	def error(self, stop_point, val):
		logging.error("{}:{}".format(stop_point, val))

	def critical(self, stop_point, val):
		logging.critical("{}:{}".format(stop_point, val))