# :coding: utf-8

import os
import maya.cmds as cmds

from imp import reload

from ..UI import Widgets
from ..UI import SettingDialog

from ..Lib import (MayaMaterial, MaterialGenerator)
from ..Lib.Log import MaterialStatusLog

reload(MayaMaterial)
reload(MaterialGenerator)


class MaterialHandlerWindow(Widgets.MaterialManagerWidgets):
    LOG = MaterialStatusLog("MayaMaterialHandler:Interface")

    def __init__(self):
        super(MaterialHandlerWindow, self).__init__()
        self._models = []
        self._materials = []
        self._colorspaces = []
        self._setting = SettingDialog.SettingDialogWidget()
        self._dir_path = None

        self.setup_widget(self)
        self._setting.setup_widget(self)

        self.table_mesh.cellClicked.connect(self.select_mesh)
        self.btn_assign.clicked.connect(self.run)
        self.btn_setting.clicked.connect(self.get_setting_dialog)
        self._setting.btn_find.clicked.connect(self.get_directory)
        self._setting.btn_load.clicked.connect(self.create_material_table)
        self._setting.btn_define.clicked.connect(self.setup_base)

    def get_setting_dialog(self):
        self._setting.show()

    def _get_materials(self):
        i = -1
        self._materials = []
        for file_name in os.listdir(self._dir_path):
            file_path = os.path.join(self._dir_path, file_name)
            tex_manager = MayaMaterial.TextureFileManager(file_path)
            tex_manager.get_texture_info()
            if self._materials != []:
                if self._materials[i]["Name"] == tex_manager.name:
                    continue
            material = {"Name": tex_manager.name, "UDIM": tex_manager.udim, "Path": file_path}
            self._materials.append(material)
            i += 1

    def create_material_table(self):
        self.LOG.message("Create Material Table")
        if self._setting.edit_directory.text() != "":
            self._get_materials()
            self._setting.table_material.set_rows(self._materials)
            self._setting.table_material.set_header()
            self.LOG.message("Completed Creation of Material Table")
        else:
            self.LOG.error("Failed Getting Texture Path")

    def get_directory(self):
        self.LOG.message("Get Directory Path")
        self._dir_path = SettingDialog.QFileDialog.getExistingDirectory()
        if self._dir_path:
            self._setting.edit_directory.setText(self._dir_path)
            self.LOG.message("Completed Getting Directory Path: {}".format(self._dir_path))
        else:
            self.LOG.error("Failed Getting Directory Path")

    def setup_base(self):
        self.LOG.message("Set Up Preparation For Base Setting")
        self._models = cmds.ls(typ="mesh")
        material_names = [item.get("Name") for item in self._materials]
        self.table_mesh.set_rows(self._models, material_names)

    def select_mesh(self, row, column):
        mesh = self.table_mesh.item(row, column).text()
        cmds.select(mesh)

    def run(self):
        self.LOG.message("Run Creation Of Materials")
        result = False
        message = "There Are No Targets"
        len_ = len(self._models)
        for i in range(len_):
            # 20220403 Start point from fixing Assigner
            assigner = MaterialGenerator.MaterialAssigner(self._models[i], self._materials[i], self._colorspaces[i])
            next(assigner.assign_materials())
            if result:
                assigner.set_ui()
                message = "Completed Creation Of Materials"
            else:
                message = "Failed Creation Of Materials"
                break
        if result:
            Widgets.QMessageBox.information(self, "Completed", message, Widgets.QMessageBox.Ok)
        else:
            Widgets.QMessageBox.critical(self, "Failed", message, Widgets.QMessageBox.Ok)