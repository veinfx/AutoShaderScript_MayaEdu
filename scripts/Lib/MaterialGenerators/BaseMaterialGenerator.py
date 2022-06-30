# coding= utf-8

import maya.cmds as cmds

from ..MayaMaterial import MayaShadingNode
from ..Log import MaterialStatusLog


class BaseMaterialManager(MayaShadingNode):
    LOG = MaterialStatusLog("MayaMaterialHandler:Module")

    def __init__(self, material, model, renderer):
        super(BaseMaterialManager, self).__init__()
        self._name = material["Name"]
        self._colorspace = material["Colorspace"]
        self._model = model
        self._renderer = renderer
        self._renderer_shader = None
        self._sg_node = None

    def create_texture_group(self, path, udim=False):
        self.LOG.message("Create Texture Group:UDIM:{0}".format(udim))
        fileNode = cmds.shadingNode("file", at=True, icm=True)
        fileNode = cmds.ls(fileNode, l=True)[0]
        self.node = fileNode
        self.set_attribute("ignoreColorSpaceFileRules", True, type_="bool")
        self.set_attribute("colorSpace", self._colorspace, type_="string")
        self.set_attribute("fileTextureName", path, type_="string")
        if udim:
            self.set_attribute("uvTilingMode", 3)

        texNode = cmds.shadingNode("place2dTexture", au=True)
        self.connect_attribute(texNode, "outUV", "uvCoord")
        self.connect_attribute(texNode, "outUvFilterSize", "uvFilterSize")
        self.connect_attribute(texNode, "vertexCameraOne")
        self.connect_attribute(texNode, "vertexUvOne")
        self.connect_attribute(texNode, "vertexUvThree")
        self.connect_attribute(texNode, "vertexUvTwo")
        self.connect_attribute(texNode, "coverage")
        self.connect_attribute(texNode, "mirrorU")
        self.connect_attribute(texNode, "mirrorV")
        self.connect_attribute(texNode, "noiseUV")
        self.connect_attribute(texNode, "offset")
        self.connect_attribute(texNode, "repeatUV")
        self.connect_attribute(texNode, "rotateFrame")
        self.connect_attribute(texNode, "rotateUV")
        self.connect_attribute(texNode, "stagger")
        self.connect_attribute(texNode, "translateFrame")
        self.connect_attribute(texNode, "wrapU")
        self.connect_attribute(texNode, "wrapV")

    def create_renderer_group(self):
        self.LOG.message("Create Renderer Group:Mesh:{0}".format(self._model))
        dag_node = cmds.ls(self._model, dag=True, s=True)
        self._sg_node = cmds.listConnections(dag_node, t="shadingEngine")[0]
        shader = cmds.listConnections(self._sg_node)
        self.node = self._renderer_shader = cmds.ls(shader, materials=True)[0]
        self.set_attribute("bumpMapType", 1)
        self.set_attribute("reflectionColor", [1.0, 1.0, 1.0], type_="double3")


class BaseMaterialAssigner:
    def __init__(self, model, material):
        self._model = model
        self._material = material

    def set_ui(self):
        opened_ui = cmds.lsUI(wnd=True)
        if "expressionEditorWin" in opened_ui:
            cmds.deleteUI("expressionEditorWin")