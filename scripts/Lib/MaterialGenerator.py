# coding= utf-8

import maya.cmds as cmds
import maya.mel as mel

from .MayaMaterial import (MayaShadingNode, TextureFileManager)
from .Log import MaterialStatusLog


class MayaMaterialManager(MayaShadingNode):
    LOG = MaterialStatusLog("MayaMaterialHandler:Module")

    def __init__(self, material, model, renderer):
        super(MayaMaterialManager, self).__init__()
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
        if udim == True:
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

    def create_vray_displacement_group(self):
        self.LOG.message("Create VRay Displacement Group")
        name = self._model + "VRayDisplacement"
        displacement_shader = cmds.createNode("VRayDisplacement", n=name)
        cmds.select(self._model)
        cmds.select(displacement_shader, add=True, ne=True)
        model = cmds.ls(sl=True)
        cmds.sets(model[0], e=True, fe=displacement_shader)
        mel.eval('vrayDispSetting("{0}");'.format(displacement_shader))
        cmds.listRelatives(displacement_shader, c=True)

    def create_prman_displacement_group(self):
        self.LOG.message("Create PRMan Displacement Group")
        name = self._model + "PRManDisplacement"
        return None

    def create_arnold_displacement_group(self):
        self.LOG.message("Create Arnold Displacement Group")
        name = self._model + "ArnoldDisplacement"
        return None

    def create_renderer_group(self):
        self.LOG.message("Create Renderer Group:Mesh:{0}".format(self._model))
        dag_node = cmds.ls(self._model, dag=True, s=True)
        self._sg_node = cmds.listConnections(dag_node, t="shadingEngine")[0]
        shader = cmds.listConnections(self._sg_node)
        self.node = self._renderer_shader = cmds.ls(shader, materials=True)[0]
        self.set_attribute("bumpMapType", 1)
        self.set_attribute("reflectionColor", [1.0, 1.0, 1.0], type_="double3")

    def set_additional_attributes(self):
        self.LOG.message("Set Additional Attributes")
        src_attr, dst_attr = None, None
        if "Aniso" in self._name and "Rotation" in self._name:
            src_attr = "outAlpha"
            dst_attr = "anisotropyRotation"
        elif "Aniso" in self._name and "Level" in self._name:
            src_attr = "outAlpha"
            dst_attr = "anisotropy"
        elif "Emissive" in self._name:
            src_attr = "outColor"
            dst_attr = "illumColor"
        elif "Base" in self._name:
            src_attr = "outColor"
            dst_attr = "color"
        elif "Height" in self._name:
            src_attr = "outAlpha"
            dst_attr = "displacement"
        elif "Metal" in self._name:
            src_attr = "outAlpha"
            dst_attr = "metalness"
        elif "Normal" in self._name:
            src_attr = "outColor"
            dst_attr = "bumpMap"
        elif "Rough" in self._name:
            src_attr = "outAlpha"
            dst_attr = "reflectionGlossiness"
        if src_attr is not None and dst_attr is not None:
            self.node, texNode = self._renderer_shader, self.node
            self.connect_attribute(texNode, src_attr, attr_=dst_attr)
        else:
            self.LOG.error("Failed Setting Addtional Attributes:SRC:{}:DST:{}".format(src_attr, dst_attr))

    def create_material(self, path, udim):
        self.create_renderer_group()
        self.create_texture_group(path, udim)
        self.set_additional_attributes()

        if "vray" in self._renderer and "height" in self._name:
            self.create_vray_displacement_group()
        elif "arnold" in self._renderer and "height" in self._name:
            self.create_arnold_displacement_group()
        elif "prman" in self._renderer and "height" in self._name:
            self.create_prman_displacement_group()


class MaterialAssigner:
    def __init__(self, model, material):
        self._model = model
        self._material = material

    def assign_materials(self):
        renderer = cmds.getAttr("defaultRenderGlobals.currentRenderer")
        mat_manager = MayaMaterialManager(self._material, self._model, renderer)
        tex_manager = TextureFileManager(self._material["Path"])
        yield mat_manager.create_material(tex_manager.path, tex_manager.udim)

    def set_ui(self):
        opened_ui = cmds.lsUI(wnd=True)
        if "expressionEditorWin" in opened_ui:
            cmds.deleteUI("expressionEditorWin")