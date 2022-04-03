# coding= utf-8

from functools import partial
from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject)
from PySide2.QtWidgets import (QWidget, QMenuBar, QToolButton, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                               QListView, QGroupBox, QComboBox, QAction, QFileDialog, QMessageBox, QTableWidget,
                               QTableWidgetItem)


class MeshTable(QTableWidget):
    def __init__(self):
        super(MeshTable, self).__init__()

    def set_header(self):
        header = ["Mesh Name", "Material"]
        len_ = len(header)
        for i in range(len_):
            header_item = QTableWidgetItem(header[i])
            self.setHorizontalHeaderItem(i, header_item)

    def set_row(self, index, mesh_name, materials):
        item_name = QTableWidgetItem(mesh_name)
        combo_material = QComboBox()
        combo_material.addItems(materials)
        self.setCellWidget(index, 1, combo_material)
        self.setItem(index, 0, item_name)

    def set_rows(self, caches, materials):
        len_ = len(caches)
        self.setColumnCount(2)
        for i in range(len_):
            self.insertRow(i)
            self.set_row(i, caches[i], materials)


class MaterialManagerWidgets(QWidget):
    def __init__(self):
        super(MaterialManagerWidgets, self).__init__()
        self.table_mesh = MeshTable()
        self.btn_assign = QPushButton()
        self.btn_setting = QPushButton()

    def setup_widget(self, manager):
        manager.setObjectName("MaterialManagerWindow")
        layout = QVBoxLayout()

        layout.addWidget(self.table_mesh)
        layout.addWidget(self.btn_assign)
        layout.addWidget(self.btn_setting)

        self.setLayout(layout)
        self.retranslate_widget(manager)
        QMetaObject.connectSlotsByName(manager)

    def retranslate_widget(self, manager):
        _objTranslate = QObject().tr
        _translate = QCoreApplication.translate
        init_obj_name = _objTranslate("MaterialManagerWindow")
        manager.setWindowTitle(_translate(init_obj_name, _objTranslate("Material Manager")))
        self.btn_assign.setText(_translate(init_obj_name, _objTranslate("Assign Material")))
        self.btn_setting.setText(_translate(init_obj_name, _objTranslate("Setting")))