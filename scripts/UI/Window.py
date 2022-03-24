# :coding: utf-8

import os

from ..UI import Widgets
from ..UI import SettingDialog
from ..Lib import MaterialGenerator
from ..Lib.Log import MaterialStatusLog


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

        self.btn_assign.clicked.connect()
        self.btn_setting.clicked.connect()
        self.btn_find.clicked.connect()
        self.btn_load.clicked.connect()
        self.btn_define.clicked.connect()

    def get_texture_path(self):
        self.LOG.message("Get Texture Path")
        path = Widgets.QFileDialog.getOpenFileName()
        if path:
            self._node.edit_file_path.setText(path)
            self.LOG.message("Completed Getting Texture Path: {}".format(path))
        else:
            self.LOG.error("Failed Getting Texture Path")

    def get_directory(self):
        self.LOG.message("Get Directory Path")
        self._dir_path = SettingDialog.QFileDialog.getExistingDirectory()
        if self._dir_path:
            self._setting.edit_root.setText(self._dir_path)
            MaterialStatusLog.message("Completed Getting Directory Path: {}".format(self._dir_path))
        else:
            MaterialStatusLog.error("Failed Getting Directory Path")

    def setup_base(self):
        self.LOG.message("Set Up Preparation For Base Setting")
        for file_name in os.listdir(self._dir_path):
            node = Widgets.MaterialNodeWidget()
            node.setup_widget(self)
            node.edit_file_path.setText(file_name)
            self._caches

    def run(self):
        self.LOG.message("Run Creation Of Materials")
        result = False
        message = "There Are No Targets"
        _len = len(self._models)
        for i in range(_len):
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