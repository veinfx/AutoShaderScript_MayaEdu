# coding= utf-8

import os
import maya.cmds as cmds

from functools import partial

from ..UI import Widgets
from ..UI import SettingDialog

from ..Lib import MayaMaterial
from ..Lib import Log

from imp import reload
reload(SettingDialog)
reload(Widgets)
reload(Log)

RENDERER = cmds.getAttr("defaultRenderGlobals.currentRenderer")
if RENDERER == "vray":
    from ..Lib.MaterialGenerators import VRayMaterialGenerator as MaterialGenerator
elif RENDERER == "arnold":
    from ..Lib.MaterialGenerators import ArnoldMaterialGenerator as MaterialGenerator
elif RENDERER == "prman":
    from ..Lib.MaterialGenerators import PRManMaterialGenerator as MaterialGenerator


class MaterialHandlerWindow(Widgets.QMainWindow):
    LOG = Log.MaterialStatusLog("MayaMaterialHandler:Interface")

    def __init__(self, parent=None):
        super(MaterialHandlerWindow, self).__init__(parent)
        self.setObjectName("MaterialHandler")
        self._models = []
        self._materials = []
        self._widget = Widgets.MaterialManagerWidgets()
        self._setting = SettingDialog.SettingDialogWidget(parent)
        self._dir_path = None

        self._widget.setup_widget(self)
        self._setting.setup_widget(self)
        self.setCentralWidget(self._widget)

        self._widget.table_mesh.cellClicked.connect(self.select_mesh)
        self._widget.btn_assign.clicked.connect(self.run)
        self._widget.btn_setting.clicked.connect(self.get_setting_dialog)
        self._setting.btn_find.clicked.connect(self.get_directory)
        self._setting.check_non_root.stateChanged.connect(self.disable_adding_material)
        self._setting.btn_add_row.clicked.connect(self.add_material)
        self._setting.btn_delete_row.clicked.connect(self._setting.table_material.delete_rows)
        self._setting.btn_delete_rows.clicked.connect(partial(self._setting.table_material.delete_rows, True))
        self._setting.btn_load.clicked.connect(self.create_material_table)
        self._setting.btn_define.clicked.connect(self.setup_base)

    def get_setting_dialog(self):
        self._setting.btn_add_row.setEnabled(False)
        self._setting.btn_delete_row.setEnabled(False)
        self._setting.btn_delete_rows.setEnabled(False)
        self._setting.show()

    def disable_adding_material(self):
        if self._setting.check_non_root.checkState():
            self._setting.btn_add_row.setEnabled(True)
            self._setting.btn_delete_row.setEnabled(True)
            self._setting.btn_delete_rows.setEnabled(True)
        else:
            self._setting.btn_add_row.setEnabled(False)
            self._setting.btn_delete_row.setEnabled(False)
            self._setting.btn_delete_rows.setEnabled(False)

    def add_material(self):
        if self._setting.check_non_root.checkState():
            self._setting.table_material.add_empty_row()
            self._setting.table_material.set_header()

    def _get_materials(self):
        i = -1
        self._materials = []
        for file_name in os.listdir(self._dir_path):
            file_path = "{0}/{1}".format(self._dir_path, file_name)
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
            self._setting.close()
            self._setting.show()
            self._widget.table_mesh.adjustSize()
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
        len_ = len(self._materials)
        for i in range(len_):
            self._materials[i]["Colorspace"] = self._setting.table_material.cellWidget(i, 5).currentText()
            self._materials[i]["DISMAP"] = self._setting.table_material.cellWidget(i, 6).isChecked()
        self._models = [mesh for mesh in cmds.ls(typ="mesh") if "polySurfaceShape" not in mesh]
        material_names = [item.get("Name") for item in self._materials]
        self._widget.table_mesh.set_rows(self._models, material_names)
        self._widget.table_mesh.set_header()
        self._setting.close()

    def select_mesh(self, row, column):
        mesh = self._widget.table_mesh.item(row, column).text()
        cmds.select(mesh)

    def run(self):
        self.LOG.message("Run Creation Of Materials")
        result = False
        message = "There Are No Targets"
        len_ = len(self._models)
        for i in range(len_):
            try:
                index = self._widget.table_mesh.cellWidget(i, 1).currentIndex()
                assigner = MaterialGenerator.MaterialAssigner(self._models[i], self._materials[index])
                next(assigner.assign_materials())
                assigner.set_ui()
                result = True
                message = "Completed Creation Of Materials"
            except:
                message = "Failed Creation Of Materials"
                break
        if result:
            Widgets.QMessageBox.information(self, "Completed", message, Widgets.QMessageBox.Ok)
        else:
            Widgets.QMessageBox.critical(self, "Failed", message, Widgets.QMessageBox.Ok)


def get_main_window():
    import shiboken2
    import maya.OpenMayaUI as OpenMayaUI

    from PySide2.QtWidgets import QWidget

    main_window_pointer = OpenMayaUI.MQtUtil.mainWindow()
    wrapper = shiboken2.wrapInstance(int(main_window_pointer), QWidget)
    return wrapper


def launch_window():
    maya_window = get_main_window()
    material_manager = MaterialHandlerWindow(maya_window)
    material_manager.show()