# coding= utf-8

import os
import json
import maya.cmds as cmds

from functools import partial
from PySide2.QtWidgets import (QMainWindow, QMessageBox, QDesktopWidget, QFileDialog, QWidget)

from ..UI import Widgets
from ..UI import SettingDialog

from ..Lib import MayaMaterial
from ..Lib import MaterialManager
from ..Lib import Log

RENDERER = cmds.getAttr("defaultRenderGlobals.currentRenderer")
if RENDERER == "vray":
    from ..Lib.MaterialGenerators import VRayMaterialGenerator as MaterialGenerator
elif RENDERER == "arnold":
    from ..Lib.MaterialGenerators import ArnoldMaterialGenerator as MaterialGenerator
elif RENDERER == "prman":
    from ..Lib.MaterialGenerators import PRManMaterialGenerator as MaterialGenerator


class MaterialHandlerWindow(QMainWindow):
    LOG = Log.MaterialStatusLog("MayaMaterialHandler:Interface")

    def __init__(self, parent=None):
        super(MaterialHandlerWindow, self).__init__(parent)
        self.setObjectName("MaterialHandler")
        self._models = []
        self._materials = []
        self._assigned_materials = {}
        self._widget = Widgets.MaterialManagerWidgets()
        self._setting = SettingDialog.SettingDialogWidget(parent)
        self._metadata = MaterialManager.MaterialMetadata()
        self._background = None
        self._dir_path = None
        self._event = None

        self._set_window_size()
        self._add_selection_callback()
        self._metadata.get_material_metadata()
        self._widget.setup_widget(self)
        self._setting.setup_widget(self)
        self.setCentralWidget(self._widget)

        self._widget.table_mesh.cellClicked.connect(self.select_mesh)
        self._widget.btn_assign.clicked.connect(self.run)
        self._widget.btn_setting.clicked.connect(self.get_setting_dialog)
        self._setting.finished.connect(self.set_dimmed)
        self._setting.btn_find.clicked.connect(self.get_directory)
        self._setting.check_non_root.stateChanged.connect(self.disable_adding_material)
        self._setting.btn_add_row.clicked.connect(self.add_material)
        self._setting.btn_delete_row.clicked.connect(self.delete_rows)
        self._setting.btn_delete_rows.clicked.connect(partial(self.delete_rows, True))
        self._setting.btn_load.clicked.connect(self.create_material_table)
        self._setting.btn_define.clicked.connect(self.setup_base)

    def _set_window_size(self):
        desktop = QDesktopWidget()
        main_monitor = desktop.screenGeometry(0)
        width = main_monitor.width() * 0.3
        height = main_monitor.height() * 0.3
        self.resize(width, height)

    def set_dimmed(self, active=False):
        if active:
            self._background = QWidget(objectName="background")
            stylesheet = """
                         #background {
                             background: rgba(64, 64, 64, 64)
                         }
                         MaterialHandlerWindow {
                             background: palette(window);
                             border: 1px outset palette(window);
                             border-radius: 5px;
                         }
                         """
            self._background.setStyleSheet(stylesheet)
            self._widget.stack.addWidget(self._background)
            self._widget.stack.setCurrentWidget(self._background)
        else:
            if self.findChild(QWidget, "background"):
                self._background.deleteLater()

    def _add_selection_callback(self):
        self._event = cmds.scriptJob(e=["SelectionChanged", self.add_selections_from_viewport])

    def delete_rows(self, all=False):
        self._setting.table_material.delete_rows(all)
        counts = self._setting.table_material.rowCount()
        if counts == 0:
            self._setting.btn_define.setEnabled(False)

    def add_selections_from_viewport(self):
        viewport_selection = cmds.ls(sl=True)
        if viewport_selection:
            len_ = self._widget.table_mesh.rowCount()
            for i in range(len_):
                item = self._widget.table_mesh.item(i, 0)
                name = cmds.listRelatives(item.text(), p=True)[0]
                if name in viewport_selection:
                    item.setSelected(True)
        else:
            self._widget.table_mesh.clearSelection()

    def set_workspace_setting(self):
        if not self._metadata.check_existence():
            workspace_path = cmds.workspace(q=True, rd=True)
            scene_path = cmds.file(q=True, exn=True)

            if workspace_path in scene_path:
                source_image_name = cmds.workspace(fre="sourceImages")
                source_image_path = "{0}/{1}".format(workspace_path, source_image_name)
                self._setting.edit_directory.setText(source_image_path)

    def get_saved_setting(self):
        if self._metadata.check_existence():
            i, j = 0, 0
            material_names = []
            with open(self._metadata.metadata_path, 'r') as metadata_file:
                material_data = json.load(metadata_file)
                self._setting.edit_directory.setText(material_data["root_texture_path"])
                for metadata in material_data["material"]:
                    material = {
                        "Name": metadata["Name"],
                        "UDIM": metadata["UDIM"],
                        "Path": metadata["Path"],
                        "Colorspace": metadata["Colorspace"],
                        "DISMAP": metadata["DISMAP"]
                    }
                    self._materials.append(material)
                    material_names.append(metadata["Name"])
                    i += 1
                self._widget.table_mesh.setColumnCount(2)
                for asset in material_data["assigned_asset"]:
                    self._widget.table_mesh.insertRow(j)
                    self._widget.table_mesh.set_row(j, asset["Name"], material_names)
                    self._widget.table_mesh.cellWidget(j, 1).setCurrentText(asset["Material"][-1])
                    self._assigned_materials[asset["Name"]] = asset["Material"]
                    j += 1
                self._widget.table_mesh.set_header()

    def get_setting_dialog(self):
        self._setting.check_non_root.setChecked(False)
        self._setting.btn_add_row.setEnabled(False)
        self._setting.btn_delete_row.setEnabled(False)
        self._setting.btn_delete_rows.setEnabled(False)
        self.set_dimmed(active=True)
        if not self._metadata.check_existence():
            self._setting.btn_define.setEnabled(False)
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
        self._setting.btn_define.setEnabled(True)

    def _get_materials(self):
        i = -1
        self._materials = []
        if self._dir_path:
            for file_name in os.listdir(self._dir_path):
                file_path = "{0}/{1}".format(self._dir_path, file_name)
                tex_manager = MayaMaterial.TextureFileManager(file_path)
                tex_manager.get_texture_info()
                if self._materials:
                    if self._materials[i]["Name"] == tex_manager.name:
                        continue
                material = {"Name": tex_manager.name, "UDIM": tex_manager.udim, "Path": file_path}
                self._materials.append(material)
                i += 1

    def create_material_table(self, load=False):
        self.LOG.message("Create Material Table")
        if not self._metadata.check_existence():
            self._get_materials()

        if self._materials:
            self._setting.table_material.set_rows(self._materials)
            self._setting.table_material.set_header()
            if not load:
                self._setting.close()
                self._setting.show()
            self._widget.table_mesh.adjustSize()
            self._setting.btn_define.setEnabled(True)
            self.LOG.message("Completed Creation of Material Table")
            return True
        return False

    def get_directory(self):
        self.LOG.message("Get Directory Path")
        directory = self._setting.edit_directory.text()
        self._dir_path = QFileDialog.getExistingDirectory(caption="Find Texture Directory", dir=directory)
        if self._dir_path:
            self._setting.edit_directory.setText(self._dir_path)
            self.LOG.message("Completed Getting Directory Path: {0}".format(self._dir_path))

    def setup_base(self):
        self.LOG.message("Set Up Preparation For Base Setting")
        len_ = len(self._materials)
        for i in range(len_):
            self._materials[i]["Colorspace"] = self._setting.table_material.cellWidget(i, 5).currentText()
            self._materials[i]["DISMAP"] = self._setting.table_material.cellWidget(i, 6).isChecked()
        self._models = [mesh for mesh in cmds.ls(typ="mesh") if "polySurfaceShape" not in mesh]
        material_names = [item.get("Name") for item in self._materials]
        row_len = self._widget.table_mesh.rowCount()
        for j in range(row_len):
            model_name = self._widget.table_mesh.item(j, 0).text()
            if model_name in self._models:
                index_ = self._models.index(model_name)
                self._models.pop(index_)
        if self._models:
            self.set_dimmed()
            self._widget.table_mesh.set_rows(self._models, material_names)
            self._widget.table_mesh.set_header()
            self._widget.btn_assign.setEnabled(True)
            self._setting.close()
            message = "Completed to create materials!"
            QMessageBox.information(self, "Completed", message, QMessageBox.Ok)
        else:
            self._setting.close()
            self.set_dimmed()
            message = "There is no models to which materials assign!"
            QMessageBox.critical(self, "Failed", message, QMessageBox.Ok)
            self.LOG.error("MaterialHandlerWindow.setup_base", message)

    def select_mesh(self, row, column):
        if self._widget.table_mesh.selectedItems():
            mesh = self._widget.table_mesh.item(row, column).text()
            cmds.select(mesh)
        else:
            cmds.select(cl=True)

    def run(self):
        self.LOG.message("Run Creation of Materials")
        result = False
        message = "There Are No Targets"
        cache = []
        len_ = self._widget.table_mesh.rowCount()
        self._metadata.collect_materials(self._materials)
        for i in range(len_):
            try:
                name = self._widget.table_mesh.item(i, 0).text()
                index = self._widget.table_mesh.cellWidget(i, 1).currentIndex()
                assigner = MaterialGenerator.MaterialAssigner(name, self._materials[index])
                next(assigner.assign_materials())
                assigner.set_ui()
                cache.extend([name, self._materials[index]["Name"]])
                result = True
                message = "Completed Creation of Materials"
            except:
                message = "Failed Creation of Materials"
                break
        if result:
            directory = self._setting.edit_directory.text()
            self._metadata.set_texture_root_path(directory)
            if self._metadata.check_existence():
                self._assigned_materials[cache[0]].append(cache[1])
            else:
                self._assigned_materials[cache[0]] = [cache[1]]
            self._metadata.save_assigned_materials(self._assigned_materials)
            self._metadata.save_metadata_file()
            QMessageBox.information(self, "Completed", message, QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Failed", message, QMessageBox.Ok)

    def showEvent(self, event):
        if not self._metadata.check_existence():
            self._widget.btn_assign.setEnabled(False)

    def closeEvent(self, event):
        cmds.scriptJob(k=self._event)


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
    material_manager.set_workspace_setting()
    material_manager.get_saved_setting()
    material_manager.create_material_table(load=True)
    material_manager.show()