# coding= utf-8

import os
import re

class TextureFileManager:
    def __init__(self, path):
        self._path = path
        self._dir_path = None
        self._name = None
        self._file_type = None

    @property
    def path(self):
        return self._path

    @property
    def dir_path(self):
        return self._dir_path

    @property
    def name(self):
        return self._name

    @property
    def file_type(self):
        return self._file_type

    def get_file_type(self):
        return self._name.endswith()

    def is_udim(self):
        return

    def check_file_type(self):
        return

    def get_texture_info(self):
        self._dir_path = os.path.dirname(self._path)
        file_name = os.path.basename(self._path)
        self._name = file_name
        self._file_type = file_name
        return