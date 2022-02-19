# coding=utf-8
# TODO: Divide Logging for Debug Mode and Result Of Running

import maya.cmds as cmds
import maya.mel as mel

from .Log import MaterialStatusLog


class MayaShadingNode:
    def __init__(self, node):
        self._node = node

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node):
        self._node = node
        MaterialStatusLog.message("Changed Node:{}".format(node))

    def set_attribute(self, attr, val, type_="int"):
        MaterialStatusLog.message("Set Attribute:{}.{}".format(self._node, attr))
        attr_name = self._node + '.' + attr
        if type_ == "int":
            cmds.setAttr(attr_name, val)
        elif type_ == "string":
            cmds.setAttr(attr_name, val, typ=type_)
        elif type_ == "bool":
            cmds.setAttr(attr_name, val)
        elif type_ == "double3":
            cmds.setAttr(attr_name, val[0], val[1], val[2], typ=type_)
        MaterialStatusLog.message("Attribute Value:{}".format(val))

    def connect_attribute(self, src, attr, attr_=None):
        MaterialStatusLog.message("Connect Attribute:SRC:{}.{}".format(src, attr))
        src_attr = src + '.' + attr
        if attr_ is None:
            dst_attr = self._node + '.' + attr
            MaterialStatusLog.message("Connect Attribute:DST:{}.{}".format(self._node, attr))
            cmds.connectAttr(src_attr, dst_attr)
        else:
            dst_attr = self._node + '.' + attr_
            MaterialStatusLog.message("Connect Attribute:DST:{}.{}".format(self._node, attr_))
            cmds.connectAttr(src_attr, dst_attr)


class MayaMaterialManager(MayaShadingNode):
    def __init__(self, name, colorspace, model, renderer):
        super(MayaMaterialManager, self).__init__()
        self._name = name
        self._colorspace = colorspace
        self._model = model
        self._renderer = renderer

    def create_texture_group(self, path, udim=False):
        MaterialStatusLog.message("Create Texture Group:UDIM:{}".format(udim))
        fileNode = cmds.shadingNode("file", at=True, icm=True)
        fileNode = cmds.ls(fileNode, l=True)[0]
        self.node = fileNode
        self.set_attribute("ignoreColorSpaceFileRules", True)
        self.set_attribute("colorspace", self._colorspace)
        self.set_attribute("fileTextureName", path)
        if udim == True:
            self.set_attribute("uvTilingMode", 3)

        texNode = cmds.shadingNode('place2dTexture', au=True)
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
        MaterialStatusLog.message("Create VRay Displacement Group")
        name = self._model + "VRayDisplacement"
        dis_shader = cmds.createNode("VRayDisplacement", n=name)
        cmds.select(self._model)
        cmds.select(dis_shader, add=True, ne=True)
        model = cmds.ls(sl=True)
        cmds.sets(model[0], e=True, fe=dis_shader)
        mel.eval('vrayDispSetting("{}");'.format(dis_shader))
        modelChecker = cmds.listRelatives(dis_shader, c=True)
        if modelChecker:
            return name
        return None

    def create_prman_displacement_group(self):
        MaterialStatusLog.message("Create PRMan Displacement Group")
        return None

    def create_arnold_displacement_group(self):
        MaterialStatusLog.message("Create Arnold Displacement Group")
        return None

    def create_renderer_group(self):
        MaterialStatusLog.message("Create Renderer Group:Mesh:{}".format(self._model))
        # TODO: add some log for check of setting
        dag_node = cmds.ls(self._model, dag=True, s=True)
        sg_node = cmds.listConnections(dag_node, t="shadingEngine")[0]
        shader = cmds.listConnections(sg_node)
        self.node = cmds.ls(shader, materials=True)[0]
        self.set_attribute("bumpMapType", 1)
        self.set_attribute("reflectionColor", [1.0, 1.0, 1.0], type_="double3")

    def set_additional_attributes(self, src):
        MaterialStatusLog.message("Set Additional Attributes")
        src_attr, dst_attr = None, None
        if "aniso" in self._name and "rotation" in self._name:
            src_attr = "outAlpha"
            dst_attr = "anisotropyRotation"
        elif "aniso" in self._name and "level" in self._name:
            src_attr = "outAlpha"
            dst_attr = "anisotropy"
        elif "emissive" in self._name:
            src_attr = "outColor"
            dst_attr = "illumColor"
        elif "base" in self._name:
            src_attr = "outColor"
            dst_attr = "color"
        elif "height" in self._name:
            src_attr = "outAlpha"
            dst_attr = "displacement"
        elif "metal" in self._name:
            src_attr = "outAlpha"
            dst_attr = "metalness"
        elif "normal" in self._name:
            src_attr = "outColor"
            dst_attr = "bumpMap"
        elif "rough" in self._name:
            src_attr = "outAlpha"
            dst_attr = "reflectionGlossiness"
        if src_attr is not None and dst_attr is not None:
            self.connect_attribute(src, src_attr, attr_=dst_attr)
        else:
            MaterialStatusLog.error("Failed Setting Addtional Attributes:SRC:{}:DST:{}".format(src_attr, dst_attr))


def create_material(name, colorspace, model, renderer, path, udim):
    material_manager = MayaMaterialManager(name, colorspace, model, renderer)
    material_manager.create_renderer_group()
    material_manager.create_texture_group(path, udim)
    material_manager.set_additional_attributes()
    if "" in renderer and "height" in name:
        dis_grp_name = material_manager.create_vray_displacement_group()
        material_manager.node = dis_grp_name
    elif "" in renderer and "height" in name:
        dis_grp_name = material_manager.create_arnold_displacement_group()
        material_manager.node = dis_grp_name
    elif "" in renderer and "height" in name:
        dis_grp_name = material_manager.create_prman_displacement_group()
        material_manager.node = dis_grp_name


def assign_materials(model, materials):
    MaterialStatusLog.message("Start Running Functions")
    model = cmds.ls(model, fl=True)[0]
    flatten_data = cmds.polyListComponentConversion(model, tf=True)
    renderer = cmds.getAttr("defaultRenderGlobals.currentRenderer")

    for name in materials.keys():

        colorspace = materials[name]
        yield create_material(name, colorspace, model, renderer, path, udim)


def set_ui():
    opened_ui = cmds.lsUI(wnd=True)
    if "expressionEditorWin" in opened_ui:
        cmds.deleteUI("expressionEditorWin")
