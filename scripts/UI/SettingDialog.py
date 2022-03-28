# coding= utf-8

from PySide2.QtCore import (QMetaObject, QCoreApplication, QObject)
from PySide2.QtWidgets import (QTableWidget, QCheckBox, QDialog, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout,
                               QComboBox, QLabel, QFileDialog)


class MaterialTable(QTableWidget):
    def __init__(self):
        super(MaterialTable, self).__init__()
        self.set_header()

    def set_header(self):
        header = ["Name", "UDIM", "Path", "Load", "Colorspace", "DISMAP"]
        self.setHorizontalHeaderLabels(header)

    def set_row(self, index):
        check_udim = QCheckBox()
        btn_load = QPushButton()
        combo_colorspace = QComboBox()
        check_dismap = QCheckBox()
        self._create_combo_colorspace(combo_colorspace)
        self.setCellWidget(index, 1, check_udim)
        self.setCellWidget(index, 3, btn_load)
        self.setCellWidget(index, 4, combo_colorspace)
        self.setCellWidget(index, 5, check_dismap)

    def _create_combo_colorspace(self, combo):
        colorspace = ["ARRI LogC", "camera Rec 709", "Sony SLog2", "Log film scam (ADX)", "Log-to-Lin (cineon)",
                      "Log-to-Lin (jzp)", "Raw", "ACES2065-1", "ACEScg", "scene-linear CIE XYZ", "scene-linear DCI-P3",
                      "scene-linear Rec 2020", "scene-linear Rec709/sRGB", "gamma 1.8 Rec 709", "gamma 2.2 Rec 709",
                      "gamma 2.4 Rec 709 (video)", "sRGB"]
        combo.addItems(colorspace)

    def set_rows(self, caches):
        for cache in caches:
            self.set_row()


class SettingDialogWidget(QDialog):
    def __init__(self):
        super(SettingDialogWidget, self).__init__(parent=None)
        self.label_setting = QLabel()
        self.check_aces = QCheckBox()
        self.edit_directory = QLineEdit()
        self.btn_find = QPushButton()
        self.edit_name_prefix = QLineEdit()
        self.btn_load = QPushButton()
        self.table_material = MaterialTable()
        self.btn_define = QPushButton()

    def setup_widget(self, dialog):
        dialog.setObjectName("SettingDialog")
        layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        path_layout = QHBoxLayout()

        path_layout.addWidget(self.edit_directory)
        path_layout.addWidget(self.btn_find)
        top_layout.addWidget(self.check_aces)
        top_layout.addLayout(path_layout)
        top_layout.addWidget(self.btn_load)
        layout.addWidget(self.label_setting)
        layout.addLayout(top_layout)
        layout.addWidget(self.table_material)
        layout.addWidget(self.btn_define)

        self.setLayout(layout)
        self.retranslate_widget(dialog)
        QMetaObject.connectSlotsByName(dialog)

    def retranslate_widget(self, dialog):
        _objTranslate = QObject().tr
        _translate = QCoreApplication.translate
        init_obj_name = _objTranslate("SettingDialog")
        dialog.setWindowTitle(_translate(init_obj_name, _objTranslate("Material Settings")))
        self.label_setting.setText(_translate(init_obj_name, _objTranslate("Material Settings")))
        self.check_aces.setText(_translate(init_obj_name, _objTranslate("ACES")))
        self.edit_directory.setText(_translate(init_obj_name, _objTranslate("Directory Path")))
        self.btn_find.setText(_translate(init_obj_name, _objTranslate("FIND")))
        self.edit_name_prefix.setText(_translate(init_obj_name, _objTranslate("Name Prefix")))
        self.btn_load.setText(_translate(init_obj_name, _objTranslate("Texture Load")))
        self.btn_define.setText(_translate(init_obj_name, _objTranslate("Define Materials")))
