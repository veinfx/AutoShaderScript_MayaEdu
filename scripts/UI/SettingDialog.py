# coding= utf-8

from PySide2.QtCore import (QMetaObject, QCoreApplication, QObject)
from PySide2.QtWidgets import (QDialog, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog)


class SettingDialogWidget(QDialog):
    def __init__(self):
        super(SettingDialogWidget, self).__init__(parent=None)
        self.edit_root = QLineEdit()
        self.btn_browser = QPushButton()
        self.edit_name_prefix = QLineEdit()
        self.btn_setup = QPushButton()

    def setup_widget(self, dialog):
        dialog.setObjectName("SettingDialog")
        layout = QVBoxLayout()
        row_layout01 = QHBoxLayout()

        row_layout01.addWidget(self.edit_root)
        row_layout01.addWidget(self.btn_browser)
        layout.addLayout(row_layout01)
        layout.addWidget(self.edit_name_prefix)
        layout.addWidget(self.btn_setup)

        self.setLayout(layout)
        self.retranslate_widget(dialog)
        QMetaObject.connectSlotsByName(dialog)

    def retranslate_widget(self, dialog):
        _objTranslate = QObject().tr
        _translate = QCoreApplication.translate
        init_obj_name = _objTranslate("SettingDialog")
        dialog.setWindowTitle(_translate(init_obj_name, _objTranslate("Settings")))
        self.edit_root.setText(_translate(init_obj_name, _objTranslate("Directory Path")))
        self.btn_browser.setText(_translate(init_obj_name, _objTranslate("BROWSE")))
        self.edit_name_prefix.setText(_translate(init_obj_name, _objTranslate("Name Prefix")))
        self.btn_setup.setText(_translate(init_obj_name, _objTranslate("RUN")))
