'''
@name: soojin_lee
@date: 2020-08-19
'''

import maya.cmds as cmds
import pymel.core as pm


class MainWindow():
    def __init__(self):
        win = pm.window(title='Auto Shader Setting')
        main_layout = pm.rowColumnLayout(nr=13)

        self.label_rough = pm.text(l='Rough Texture')
        pm.setParent(main_layout)
        rough_layout = pm.rowLayout(nc=2)        
        self.rough_path = pm.textFieldGrp()
        self.btn_rough = pm.button(l='BROWSE', c=self._get_rough_path)        
        pm.setParent(main_layout)
        self.rough_color = self.create_colorspace_menu()

        self.label_base = pm.text(l='Base Texture')        
        pm.setParent(main_layout)
        base_layout = pm.rowLayout(nc=2)        
        self.base_path = pm.textFieldGrp()
        self.btn_base = pm.button(l='BROWSE', c=self._get_base_path)        
        pm.setParent(main_layout)
        self.base_color = self.create_colorspace_menu()

        self.label_normal = pm.text(l='Normal Texture')        
        pm.setParent(main_layout)
        normal_layout = pm.rowLayout(nc=2)        
        self.normal_path = pm.textFieldGrp()
        self.btn_normal = pm.button(l='BROWSE', c=self._get_normal_path)        
        pm.setParent(main_layout)
        self.normal_color = self.create_colorspace_menu()

        self.label_metal = pm.text(l='Metal Texture')        
        pm.setParent(main_layout)
        metal_layout = pm.rowLayout(nc=2)        
        self.metal_path = pm.textFieldGrp()
        self.btn_metal = pm.button(l='BROWSE', c=self._get_metal_path)        
        pm.setParent(main_layout)
        self.metal_color = self.create_colorspace_menu()

        self.btn_main = pm.button(l='RUN', bgc=(0.3, 0.6, 0.1), c=self._create_shader_nodes)

        win.show()

    def create_colorspace_menu(self):
        colorspace_items = ('ARRI LogC', 'camera Rec 709', 'Sony SLog2', 
                            'Log film scam (ADX)', 'Log-to-Lin (cineon)',
                            'Log-to-Lin (jzp)', 'Raw', 'ACES2065-1', 'ACEScg',
                            'scene-linear CIE XYZ', 'scene-linear DCI-P3',
                            'scene-linear Rec 2020', 'scene-linear Rec709/sRGB',
                            'gamma 1.8 Rec 709', 'gamma 2.2 Rec 709', 'gamma 2.4 Rec 709 (video)',
                            'sRGB')        
        menu = pm.optionMenuGrp(l='COLORSPACE')
        for item in colorspace_items:
            pm.menuItem(l=item)        
        return menu

    def _get_rough_path(self, *args):
        return self.get_rough_path()

    def get_rough_path(self):
        file_name = pm.fileDialog()
        self.rough_path.setText(file_name)

    def _get_base_path(self, *args):
        return self.get_base_path()

    def get_base_path(self):
        file_name = pm.fileDialog()
        self.base_path.setText(file_name)

    def _get_normal_path(self, *args):
        return self.get_normal_path()

    def get_normal_path(self):
        file_name = pm.fileDialog()
        self.normal_path.setText(file_name)

    def _get_metal_path(self, *args):
        return self.get_metal_path()

    def get_metal_path(self):
        file_name = pm.fileDialog()
        self.metal_path.setText(file_name)

    def create_texture_file_node(self, file_name):
        file_node = cmds.shadingNode('file', at=True, icm=True)
        file_node = cmds.ls(file_node)[0]
        cmds.setAttr('{}.fileTextureName'.format(file_node), file_name, typ='string')    
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

    def _create_shader_nodes(self, *args):
        return self.create_shader_nodes()

    def create_shader_nodes(self):
        img_rough = self.rough_path.getText()
        img_base = self.base_path.getText()
        img_normal = self.normal_path.getText()
        img_metal = self.metal_path.getText()

        rough_node = self.create_texture_file_node(img_rough)
        base_node = self.create_texture_file_node(img_base)
        normal_node = self.create_texture_file_node(img_normal)
        metal_node = self.create_texture_file_node(img_metal) 

        vray_node = cmds.shadingNode('VRayMtl', au=True)
        shading_engine = cmds.shadingNode('shadingEngine', n='VRayMtl1SG', au=True)

        cmds.connectAttr('{}.outAlpha'.format(rough_node), '{}.reflectionGlossiness'.format(vray_node))       
        cmds.connectAttr('{}.outColor'.format(base_node), '{}.color'.format(vray_node))       
        cmds.connectAttr('{}.outColor'.format(normal_node), '{}.bumpMap'.format(vray_node))       
        cmds.connectAttr('{}.outAlpha'.format(metal_node), '{}.metalness'.format(vray_node))           

        cmds.connectAttr('{}.outColor'.format(vray_node), '{}.surfaceShader'.format(shading_engine))
        

main = MainWindow()                     