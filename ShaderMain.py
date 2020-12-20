'''
@name: soojin_lee
@date: 2020-08-19
@adjusted_date: 2020-12-20
'''

import glob
import maya.cmds as cmds

import ShaderSetup as shader_setup


class MainWindow(object):
    def __init__(self):
        self._map_dict = {'base': None, 'height': None, 'metallic': None, 'normal': None, 'roughness': None}
        self.set_window()

    def set_window(self):
        window_id = "autoShaderSetting"

        if cmds.window(window_id, ex=True):
            cmds.deleteUI(window_id)

        window = cmds.window(window_id, t='Auto Shader Setting')
        cmds.columnLayout(adj=True, p=window)

        self.create_object_viewer()

        self.root_path = None
        cmds.textField('rootDirPath')
        self.btn_browser = cmds.button(l='BROWSE', c=self.get_path)

        self.label_base = cmds.text(l='Base Texture')
        self.base_color = self.create_colorspace_menu('base')

        self.label_height = cmds.text(l='Height Texture')
        self.height_color = self.create_colorspace_menu('height')

        self.label_rough = cmds.text(l='Rough Texture')
        self.rough_color = self.create_colorspace_menu('roughness')

        self.label_normal = cmds.text(l='Normal Texture')
        self.normal_color = self.create_colorspace_menu('normal')

        self.label_metal = cmds.text(l='Metallic Texture')
        self.metal_color = self.create_colorspace_menu('metallic')

        self.btn_main = cmds.button(l='RUN', bgc=(0.3, 0.6, 0.1), c=self.create_shader_nodes)

        cmds.showWindow(window)

    def create_object_viewer(self, *args):
        object_mesh = cmds.ls(dag=True, s=True, typ='mesh')
        transforms = [cmds.listRelatives(model, p=True)[0] for model in object_mesh if cmds.nodeType(model) != 'camera']
        cmds.textScrollList('objectViewer', a=transforms, ams=True)

    def create_colorspace_menu(self, color_type):
        colorspace = {'arri_logc': 'ARRI LogC', 'camera_rec709': 'camera Rec 709',
                      'sony_slog2': 'Sony SLog2', 'log_film_scam': 'Log film scam (ADX)',
                      'cineon': 'Log-to-Lin (cineon)', 'jzp': 'Log-to-Lin (jzp)',
                      'raw': 'Raw', 'aces2065_1': 'ACES2065-1', 'aces_cg': 'ACEScg',
                      'cie_xyz': 'scene-linear CIE XYZ', 'dci_p3': 'scene-linear DCI-P3',
                      'rec2020': 'scene-linear Rec 2020',
                      'rec709_srgb': 'scene-linear Rec709/sRGB', 'gamma1.8': 'gamma 1.8 Rec 709',
                      'gamma2.2': 'gamma 2.2 Rec 709', 'gamma2.4': 'gamma 2.4 Rec 709 (video)',
                      'sRGB': 'sRGB'}

        default_set = {'base': 'sRGB', 'height': 'Raw', 'metallic': 'Raw', 'normal': 'sRGB', 'roughness': 'Raw'}
        menu = cmds.optionMenu(color_type, l='COLORSPACE', en=True)
        for key in colorspace.keys():
            cmds.menuItem(key, l=colorspace[key])
        cmds.optionMenu(color_type, e=True, v=default_set[color_type])
        return menu

    def get_path(self, *args):
        file_name = cmds.fileDialog2(fm=3)[0]
        cmds.textField('rootDirPath', e=True, tx=str(file_name))
        self.root_path = cmds.textField('rootDirPath', q=True, tx=True)

        maps = ['Base', 'base', 'Height', 'height', 'Metallic', 'metallic',
                     'Normal', 'normal', 'Roughness', 'roughness']
        map_list = glob.glob('{}/*_{}*'.format(self.root_path, maps))

        objects = cmds.textScrollList('objectViewer', q=True, si=True)
        size = len(maps)
        for i in range(0, size, 2):
            map_path = filter(lambda x: maps[i] in x or maps[i+1] in x, map_list)
            map_files = filter(lambda x: '1001' in x, map_path)
            self._map_dict[maps[i+1]] = map_files
        for key in self._map_dict.keys():
            print self._map_dict[key]


    def create_shader_nodes(self, *args):
        objects = cmds.textScrollList('objectViewer', q=True, si=True)
        for model in objects:
            shader_setup.create_shaders(model, self._map_dict)