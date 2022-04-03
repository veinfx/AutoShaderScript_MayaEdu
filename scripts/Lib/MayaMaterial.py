# coding=utf-8

import os
import re
import maya.cmds as cmds


class MayaShadingNode:
    def __init__(self, node):
        self._node = node

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node):
        self._node = node

    def set_attribute(self, attr, val, type_="int"):
        attr_name = self._node + '.' + attr
        if type_ == "int":
            cmds.setAttr(attr_name, val)
        elif type_ == "string":
            cmds.setAttr(attr_name, val, typ=type_)
        elif type_ == "bool":
            cmds.setAttr(attr_name, val)
        elif type_ == "double3":
            cmds.setAttr(attr_name, val[0], val[1], val[2], typ=type_)

    def connect_attribute(self, src, attr, attr_=None):
        src_attr = src + '.' + attr
        if attr_ is None:
            dst_attr = self._node + '.' + attr
            cmds.connectAttr(src_attr, dst_attr)
        else:
            dst_attr = self._node + '.' + attr_
            cmds.connectAttr(src_attr, dst_attr)


class TextureFileManager:
    FILE_TYPE = {"jpg", "jpeg", "png", "PNG", "exr", "tx", "tex", "tiff"}

    def __init__(self, path):
        self._path = path
        self._dir_path = None
        self._name = None
        self._file_type = None
        self._udim = False

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

    @property
    def udim(self):
        return self._udim

    def get_file_name(self, value):
        name_elements = value.split('.')
        name_set = set(name_elements)
        if name_set.intersection(self.FILE_TYPE):
            self._name = name_elements[0]
        else:
            print("Error: This can't be defined as a <file name>! Check your values! - {0}".format(value))

    def get_file_type(self, value):
        name_elements = value.split('.')
        name_set = set(name_elements)
        if name_set.intersection(self.FILE_TYPE):
            self._file_type = name_elements[-1]
        else:
            print("Error: This can't be defined as a <file type>! Check your values! - {0}".format(value))

    def is_udim(self, value):
        if '.' in value:
            division = value.split('.')
            number_filter = re.search("\d\d\d\d", division[1])
            if number_filter:
                self._udim = True

    def get_texture_info(self):
        self._dir_path = os.path.dirname(self._path)
        file_name = os.path.basename(self._path)
        self.get_file_name(file_name)
        self.get_file_type(file_name)
        self.is_udim(file_name)