"""
@name: soojin_lee
@date: 2020-08-19
@adjusted_date: 2020-12-20
"""

import re
import os
import maya.cmds as cmds
import maya.mel as mel


class ShaderSetter(object):
    def __init__(self, model, maps):
        self._model = model
        self._maps = maps
        self._vray_shader = None
        self._sg_node = None

    def check_sequential_texture(self, color_type, shader_name):
        texture = [name for name in self._maps[color_type] if shader_name in name]
        if len(texture) == 1:
            tx_type = 'non_udim'
        else:
            tx_type = 'udim'
        return tx_type

    def create_texture_file_node(self, color_type):
        file_node = cmds.shadingNode('file', at=True, icm=True)
        file_node = cmds.ls(file_node, l=True)[0]
        color = cmds.optionMenu(color_type, q=True, v=True)
        cmds.setAttr('{}.ignoreColorSpaceFileRules'.format(file_node), True)
        cmds.setAttr('{}.colorSpace'.format(file_node), color, typ='string')

        data = filter(lambda x: self._vray_shader in x, self._maps[color_type])
        if data != []:
            tx_type = self.check_sequential_texture(color_type, self._vray_shader)
            if self._vray_shader in data[0] and tx_type == 'udim':
                cmds.setAttr('{}.fileTextureName'.format(file_node), data[0], typ='string')
                cmds.setAttr('{}.uvTilingMode'.format(file_node), 3)
            else:
                cmds.setAttr('{}.fileTextureName'.format(file_node), data[0], typ='string')
        else:
            cmds.delete(file_node)
            return None
        tex_node = cmds.shadingNode('place2dTexture', au=True)
        tex_attrs = ('outUV', 'outUvFilterSize')
        file_attrs = ('uvCoord', 'uvFilterSize')
        for i in range(2):
            cmds.connectAttr('{}.{}'.format(tex_node, tex_attrs[i]), '{}.{}'.format(file_node, file_attrs[i]))
        common_attrs = ('vertexCameraOne', 'vertexUvOne', 'vertexUvThree', 'vertexUvTwo', 'coverage', \
                        'mirrorU', 'mirrorV', 'noiseUV', 'offset', 'repeatUV', 'rotateFrame', 'rotateUV', \
                        'stagger', 'translateFrame', 'wrapU', 'wrapV')
        for attr in common_attrs:
            cmds.connectAttr('{}.{}'.format(tex_node, attr), '{}.{}'.format(file_node, attr))
        return file_node

    def find_shader(self):
        dag_node = cmds.ls(self._model, dag=True, s=True)
        self._sg_node = cmds.listConnections(dag_node, t='shadingEngine')[0]
        shader = cmds.listConnections(self._sg_node)
        self._vray_shader = cmds.ls(shader, materials=True)[0]
        cmds.setAttr('{}.bumpMapType'.format(self._vray_shader), 1)
        cmds.setAttr('{}.reflectionColor'.format(self._vray_shader), 1.0, 1.0, 1.0, typ='double3')

    def connect_attrs(self, nodes=None, aniso_rotation=None, aniso_level=None, emissive=None):
        cmds.connectAttr('{}.outColor'.format(nodes[1]), '{}.color'.format(self._vray_shader))
        cmds.connectAttr('{}.outAlpha'.format(nodes[2]), '{}.displacement'.format(nodes[0]))
        cmds.connectAttr('{}.outAlpha'.format(nodes[5]), '{}.reflectionGlossiness'.format(self._vray_shader))
        cmds.connectAttr('{}.outColor'.format(nodes[4]), '{}.bumpMap'.format(self._vray_shader))
        cmds.connectAttr('{}.outAlpha'.format(nodes[3]), '{}.metalness'.format(self._vray_shader))
        if emissive is not None:
            cmds.connectAttr('{}.outColor'.format(emissive), '{}.illumColor'.format(self._vray_shader))
        if aniso_level is not None:
            cmds.connectAttr('{}.outAlpha'.format(aniso_level), '{}.anisotropy'.format(self._vray_shader))
        if aniso_rotation is not None:
            cmds.connectAttr('{}.outAlpha'.format(aniso_rotation), '{}.anisotropyRotation'.format(self._vray_shader))

    def create_shaders(self):
        model = cmds.ls(self._model, fl=True)[0]
        flatten_data = cmds.polyListComponentConversion(model, tf=True)
        base_node = self.create_texture_file_node('base')
        height_node = self.create_texture_file_node('height')
        metal_node = self.create_texture_file_node('metallic')
        normal_node = self.create_texture_file_node('normal')
        rough_node = self.create_texture_file_node('roughness')
        anisotropy_angle_node = self.create_texture_file_node('anisotropy_angle')
        anisotropy_level_node = self.create_texture_file_node('anisotropy_level')
        emissive_node = self.create_texture_file_node('emissive')

        dismap_node = cmds.shadingNode('displacementShader', asShader=True)

        node_list = [dismap_node, base_node, height_node, metal_node, normal_node, rough_node]
        aniso_r_data, aniso_l_data, emiss_data = anisotropy_angle_node, anisotropy_level_node, emissive_node
        if anisotropy_angle_node is None:
            del anisotropy_angle_node
            aniso_r_data = None
        if anisotropy_level_node is None:
            del anisotropy_level_node
            aniso_l_data = None
        if emissive_node is None:
            del emissive_node
            emiss_data = None
        self.connect_attrs(nodes=node_list, aniso_rotation=aniso_r_data, aniso_level=aniso_l_data, emissive=emiss_data)

        cmds.connectAttr('{}.displacement'.format(dismap_node), '{}.displacementShader'.format(self._sg_node))
        cmds.connectAttr('{}.outColor'.format(self._vray_shader), '{}.surfaceShader'.format(self._sg_node), f=True)

        cmds.setAttr('{}.useRoughness'.format(self._vray_shader), True)

        cmds.select(self._vray_shader, add=True)
        cmds.sets(flatten_data, e=True, fe=self._sg_node)
        cmds.select(self._vray_shader, d=True)

    def create_dismap(self):
        dis_shader = cmds.createNode('VRayDisplacement', n=self._model+'_disp')
        cmds.select(self._model)
        cmds.select(dis_shader, add=True, ne=True)
        model = cmds.ls(sl=True)
        cmds.sets(model[0], e=True, fe=dis_shader)
        mel.eval('vrayDispSetting("{}");'.format(dis_shader))

        try:
            model_checker = cmds.listRelatives(dis_shader, c=True)
            if model_checker != []:
                return True
        except:
            print '**  Failed to create Displacement shader!  **'
            return False