# :coding: utf-8

import os

from ..UI import Widgets
from ..UI import SettingDialog
from ..Lib import MayaMaterial
from ..Lib.Log import MaterialStatusLog


class MaterialHandlerWindow(Widgets.MaterialManagerWidgets):
    def __init__(self):
        super(MaterialHandlerWindow, self).__init__()
        self._models = []
        self._caches = []
        self._setting = SettingDialog.SettingDialogWidget()
        self._dir_path = None

        self.setup_widget(self)
        self._setting.setup_widget(self)

        self.act_setting.triggered.connect(self._setting.show)
        self._setting.btn_browser.clicked.connect(self.get_directory)
        self._setting.btn_setup.clicked.connect(self.setup_base)
        self.btn_run.clicked.connect(self.run)

    def get_texture_path(self):
        MaterialStatusLog.message("Get Texture Path")
        path = Widgets.QFileDialog.getOpenFileName()
        if path:
            self._node.edit_file_path.setText(path)
            MaterialStatusLog.message("Completed Getting Texture Path: {}".format(path))
        else:
            MaterialStatusLog.error("Failed Getting Texture Path")

    def get_directory(self):
        MaterialStatusLog.message("Get Directory Path")
        self._dir_path = SettingDialog.QFileDialog.getExistingDirectory()
        if self._dir_path:
            self._setting.edit_root.setText(self._dir_path)
            MaterialStatusLog.message("Completed Getting Directory Path: {}".format(self._dir_path))
        else:
            MaterialStatusLog.error("Failed Getting Directory Path")

    def setup_base(self):
        MaterialStatusLog.message("Set Up Preparation For Base Setting")
        for file_name in os.listdir(self._dir_path):
            node = Widgets.MaterialNodeWidget()
            node.setup_widget(self)
            node.edit_file_path.setText(file_name)
            self._caches

    def run(self):
        MaterialStatusLog.message("Run Creation Of Materials")
        result = False
        message = "There Are No Targets"
        _len = len(self._models)
        for i in range(_len):
            next(MayaMaterial.assign_materials(self._models[i], self._caches[i]))
            if result:
                message = "Completed Creation Of Materials"
            else:
                message = "Failed Creation Of Materials"
                break
        if result:
            MayaMaterial.set_ui()
            Widgets.QMessageBox.information(self, "Completed", message, Widgets.QMessageBox.Ok)
        else:
            Widgets.QMessageBox.critical(self, "Failed", message, Widgets.QMessageBox.Ok)