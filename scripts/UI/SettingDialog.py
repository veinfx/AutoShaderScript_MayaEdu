# coding= utf-8

from functools import partial
from PySide2.QtCore import (QMetaObject, QCoreApplication, QObject)
from PySide2.QtWidgets import (QTableWidget, QCheckBox, QDialog, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout,
                               QComboBox, QLabel, QFileDialog, QTableWidgetItem, QSizePolicy, QAbstractScrollArea)


class MaterialTable(QTableWidget):
    def __init__(self):
        super(MaterialTable, self).__init__()

    def set_header(self):
        header = ["Name", "UDIM", "Path", "File Path", "Colorspace", "DISMAP"]
        len_ = len(header)
        for i in range(len_):
            header_item = QTableWidgetItem(header[i])
            self.setHorizontalHeaderItem(i, header_item)

    def set_row(self, index, name, udim, file_path):
        item_name = QTableWidgetItem(name)
        item_path = QTableWidgetItem(file_path)
        check_udim = QCheckBox()
        btn_load = QPushButton()
        combo_colorspace = QComboBox()
        check_dismap = QCheckBox()
        self._create_combo_colorspace(combo_colorspace)
        self.setCellWidget(index, 1, check_udim)
        self.setCellWidget(index, 3, btn_load)
        self.setCellWidget(index, 4, combo_colorspace)
        self.setCellWidget(index, 5, check_dismap)
        self.setItem(index, 0, item_name)
        self.setItem(index, 2, item_path)
        check_udim.setChecked(udim)
        btn_load.clicked.connect(partial(self.get_file_path, index))

    def _create_combo_colorspace(self, combo):
        colorspace = ["ARRI LogC", "camera Rec 709", "Sony SLog2", "Log film scam (ADX)", "Log-to-Lin (cineon)",
                      "Log-to-Lin (jzp)", "Raw", "ACES2065-1", "ACEScg", "scene-linear CIE XYZ", "scene-linear DCI-P3",
                      "scene-linear Rec 2020", "scene-linear Rec709/sRGB", "gamma 1.8 Rec 709", "gamma 2.2 Rec 709",
                      "gamma 2.4 Rec 709 (video)", "sRGB"]
        combo.addItems(colorspace)

    def get_file_path(self, row):
        from ..Lib.MayaMaterial import TextureFileManager

        file_path = QFileDialog.getOpenFileName(self, "Get File Path")
        if file_path[0] != '':
            check_udim = self.cellWidget(row, 1)
            tex_manager = TextureFileManager(file_path[0])
            tex_manager.get_texture_info()
            item_path = QTableWidgetItem(file_path[0])
            item_name = QTableWidgetItem(tex_manager.name)
            self.setItem(row, 0, item_name)
            self.setItem(row, 2, item_path)
            check_udim.setChecked(tex_manager.udim)
            self.resizeColumnToContents(2)
            self.sizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def get_current_index(self):
        row_count = self.rowCount() + 1
        index = 0
        if row_count != 0:
            index = row_count - 1
        return index

    def add_empty_row(self):
        index = self.get_current_index()
        self.setColumnCount(6)
        self.insertRow(index)
        self.set_row(index, '', False, '')
        self.retranslate_cell_widgets(index)

    def set_rows(self, caches):
        len_ = len(caches)
        self.setColumnCount(6)
        for i in range(len_):
            index = self.get_current_index()
            self.insertRow(index)
            self.set_row(index, caches[i]["Name"], caches[i]["UDIM"], caches[i]["Path"])
            self.retranslate_cell_widgets(index)

    def retranslate_cell_widgets(self, index):
        _objTranslate = QObject().tr
        _translate = QCoreApplication.translate
        init_obj_name = _objTranslate("SettingDialog")
        self.cellWidget(index, 1).setText(_translate(init_obj_name, _objTranslate("UDIM")))
        self.cellWidget(index, 3).setText(_translate(init_obj_name, _objTranslate("Load")))
        self.cellWidget(index, 5).setText(_translate(init_obj_name, _objTranslate("DISMAP")))


class SettingDialogWidget(QDialog):
    def __init__(self, parent=None):
        super(SettingDialogWidget, self).__init__(parent)
        self.label_setting = QLabel()
        self.check_aces = QCheckBox()
        self.edit_directory = QLineEdit()
        self.btn_find = QPushButton()
        self.edit_name_prefix = QLineEdit()
        self.check_non_root = QCheckBox()
        self.btn_add_row = QPushButton()
        self.btn_load = QPushButton()
        self.table_material = MaterialTable()
        self.btn_define = QPushButton()

    def setup_widget(self, dialog):
        dialog.setObjectName("SettingDialog")
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        path_layout = QHBoxLayout()
        option_layout = QHBoxLayout()

        path_layout.addWidget(self.edit_directory)
        path_layout.addWidget(self.btn_find)
        option_layout.addWidget(self.check_non_root)
        option_layout.addWidget(self.btn_add_row)
        top_layout.addWidget(self.check_aces)
        top_layout.addLayout(option_layout)
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
        self.check_non_root.setText(_translate(init_obj_name, _objTranslate("Enable To Load Paths From Non Root")))
        self.btn_add_row.setText(_translate(init_obj_name, _objTranslate("ADD MATERIAL")))
        self.edit_name_prefix.setText(_translate(init_obj_name, _objTranslate("Name Prefix")))
        self.btn_load.setText(_translate(init_obj_name, _objTranslate("Texture Load")))
        self.btn_define.setText(_translate(init_obj_name, _objTranslate("Define Materials")))
