'''
@name: soojin_lee
@date: 2020-08-19
@adjusted_date: 2020-12-20
'''

import re
import os
import maya.cmds as cmds


class ShaderSetter(object):
    def __init__(self, model, maps):
        self._model = model
        self._maps = maps

    def check_sequential_texture(self, color_type, shader_name):
        texture = [name for name in self._maps[color_type] if shader_name in name]
        if len(texture) == 1:
            print '----  non udim model: {}  ----'.format(self._model)
            tx_type = 'non_udim'
        else:
            tx_type = 'udim'
        return tx_type

    def create_texture_file_node(self, color_type, shader_info):
        file_node = cmds.shadingNode('file', at=True, icm=True)
        file_node = cmds.ls(file_node, l=True)[0]
        color = cmds.optionMenu(color_type, q=True, v=True)
        cmds.setAttr('{}.ignoreColorSpaceFileRules'.format(file_node), True)
        cmds.setAttr('{}.colorSpace'.format(file_node), color, typ='string')

        data = filter(lambda x: shader_info in x, self._maps[color_type])
        if data != []:
            tx_type = self.check_sequential_texture(color_type, shader_info)
            if shader_info in data[0] and tx_type == 'udim':
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
        sg_node = cmds.listConnections(dag_node, t='shadingEngine')[0]
        shader = cmds.listConnections(sg_node)
        vray_shader = cmds.ls(shader, materials=True)[0]
        cmds.setAttr('{}.bumpMapType'.format(vray_shader), 1)
        cmds.setAttr('{}.reflectionColor'.format(vray_shader), 1.0, 1.0, 1.0, typ='double3')
        return vray_shader, sg_node

    def connect_attrs(self, nodes):
        cmds.connectAttr('{}.outColor'.format(nodes[2]), '{}.color'.format(nodes[0]))
        cmds.connectAttr('{}.outAlpha'.format(nodes[3]), '{}.displacement'.format(nodes[1]))
        cmds.connectAttr('{}.outAlpha'.format(nodes[6]), '{}.reflectionGlossiness'.format(nodes[0]))
        cmds.connectAttr('{}.outColor'.format(nodes[5]), '{}.bumpMap'.format(nodes[0]))
        cmds.connectAttr('{}.outAlpha'.format(nodes[4]), '{}.metalness'.format(nodes[0]))
        if len(nodes) > 7:
            cmds.connectAttr('{}.outColor'.format(nodes[9]), '{}.illumColor'.format(nodes[0]))
            cmds.connectAttr('{}.outAlpha'.format(nodes[8]), '{}.anisotropy'.format(nodes[0]))
            cmds.connectAttr('{}.outAlpha'.format(nodes[7]), '{}.anisotropyRotation'.format(nodes[0]))

    def create_shaders(self):
        model = cmds.ls(self._model, fl=True)[0]
        flatten_data = cmds.polyListComponentConversion(model, tf=True)
        vray_node, shading_engine = self.find_shader()
        base_node = self.create_texture_file_node('base', vray_node)
        height_node = self.create_texture_file_node('height', vray_node)
        metal_node = self.create_texture_file_node('metallic', vray_node)
        normal_node = self.create_texture_file_node('normal', vray_node)
        rough_node = self.create_texture_file_node('roughness', vray_node)
        anisotropy_angle_node = self.create_texture_file_node('anisotropy_angle', vray_node)
        anisotropy_level_node = self.create_texture_file_node('anisotropy_level', vray_node)
        emissive_node = self.create_texture_file_node('emissive', vray_node)

        dismap_node = cmds.shadingNode('displacementShader', asShader=True)

        nodes = [vray_node, dismap_node, base_node, height_node, metal_node, normal_node, rough_node]
        for addition in (anisotropy_angle_node, anisotropy_level_node, emissive_node):
            if addition is None:
                del addition
            else:
                nodes.append(addition)

        self.connect_attrs(nodes)

        cmds.connectAttr('{}.displacement'.format(dismap_node), '{}.displacementShader'.format(shading_engine))
        cmds.connectAttr('{}.outColor'.format(vray_node), '{}.surfaceShader'.format(shading_engine), f=True)

        cmds.setAttr('{}.useRoughness'.format(vray_node), True)

        cmds.select(vray_node, add=True)
        cmds.sets(flatten_data, e=True, fe=shading_engine)
        cmds.select(vray_node, d=True)

    def create_dismap(self):
        dis_shader = cmds.createNode('VRayDisplacement')
        cmds.select(self._model)
        cmds.select(dis_shader, add=True, ne=True)
        model = cmds.ls(sl=True)
        cmds.sets(model[0], e=True, fe=dis_shader)

        try:
            model_checker = cmds.listRelatives(dis_shader, c=True)
            if model_checker != []:
                return True
        except:
            print '**  Failed to create Displacement shader!  **'
            return False