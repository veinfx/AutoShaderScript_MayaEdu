# coding= utf-8

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject)
from PySide2.QtWidgets import (QWidget, QMenuBar, QToolButton, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                               QListView, QGroupBox, QComboBox, QAction, QFileDialog, QMessageBox)
from PySide2.QtWidgets import (QTableWidget)


class MaterialManagerWidgets(QWidget):
    def __init__(self):
        super(MaterialManagerWidgets, self).__init__(parent=None)
        self.table_mesh = QTableWidget()
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