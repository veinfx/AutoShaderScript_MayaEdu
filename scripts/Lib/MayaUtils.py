# coding=utf-8

import maya.cmds as cmds


class MayaTextureUdim:
    def __init__(self, mesh):
        self._mesh = mesh

    def getUdimNumber(self):
        return