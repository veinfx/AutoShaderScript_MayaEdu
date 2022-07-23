# coding= utf-8

import maya.cmds as cmds
import maya.mel as mel

from ..MaterialGenerators.BaseMaterialGenerator import (BaseMaterialManager, BaseMaterialAssigner)
from ..MayaMaterial import TextureFileManager
from ..Log import MaterialStatusLog


class MayaMaterialManager(BaseMaterialManager):
    LOG = MaterialStatusLog("MayaMaterialHandler:Module")

    def __init__(self, material, model, renderer):
        super(MayaMaterialManager, self).__init__(material, model, renderer)

    def create_displacement_group(self):
        self.LOG.message("Create VRay Displacement Group")
        name = self._model + "vrayDisplacement"
        displacement_shader = cmds.createNode("VRayDisplacement", n=name)
        cmds.select(self._model)
        cmds.select(displacement_shader, add=True, ne=True)
        model = cmds.ls(sl=True)
        cmds.sets(model[0], e=True, fe=displacement_shader)
        mel.eval('vrayDispSetting("{0}");'.format(displacement_shader))
        cmds.listRelatives(displacement_shader, c=True)

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
            message = "Failed Setting Addtional Attributes:SRC:{}:DST:{}".format(src_attr, dst_attr)
            self.LOG.error("MayaMaterialManager.set_additional_attributes", message)

    def create_material(self, path, udim):
        self.create_renderer_group()
        self.create_texture_group(path, udim)
        self.set_additional_attributes()

        if "height" in self._name:
            self.create_displacement_group()


class MaterialAssigner(BaseMaterialAssigner):
    def __init__(self, model, material):
        super(MaterialAssigner, self).__init__(model, material)

    def assign_materials(self):
        renderer = cmds.getAttr("defaultRenderGlobals.currentRenderer")
        mat_manager = MayaMaterialManager(self._material, self._model, renderer)
        tex_manager = TextureFileManager(self._material["Path"])
        yield mat_manager.create_material(tex_manager.path, tex_manager.udim)