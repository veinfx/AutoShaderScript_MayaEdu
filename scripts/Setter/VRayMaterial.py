# :coding: utf-8

import maya.cmds as cmds
import maya.mel as mel

from .. import AssetInfo

class VRayMaterialHandler(AssetInfo.Asset):
    def __init__(self, model, material, colorspace):
        self._model = model
        self._material = material
        self._colorspace = colorspace

    def create_displacement(self):
        dis_shader = cmds.createNode('VRayDisplacement', n=self._model + '_disp')
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

    def run(self):
        self.create_displacement()