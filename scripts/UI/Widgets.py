# coding= utf-8

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject)
from PySide2.QtWidgets import (QWidget, QMenuBar, QToolButton, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                               QListView, QGroupBox, QComboBox, QAction, QFileDialog, QMessageBox)


class MaterialNodeWidget(QWidget):
    def __init__(self):
        super(MaterialNodeWidget, self).__init__(parent=None)
        self.icon_file = QToolButton()
        self.edit_file_path = QLineEdit()
        self.btn_browser = QPushButton()
        self.combo_colorspace = QComboBox()
        self.icon_del = QToolButton()

    def setup_widget(self, node):
        node.setObjectName("MaterialNode")
        layout = QHBoxLayout()
        option_layout = QVBoxLayout()
        path_layout = QHBoxLayout()
        self._create_combo()

        path_layout.addWidget(self.edit_file_path)
        path_layout.addWidget(self.btn_browser)
        option_layout.addLayout(path_layout)
        option_layout.addWidget(self.combo_colorspace)
        layout.addWidget(self.icon_file)
        layout.addLayout(option_layout)
        layout.addWidget(self.icon_del)

        self.setLayout(layout)
        self.retranslate_widget(node)
        QMetaObject.connectSlotsByName(node)

    def retranslate_widget(self, node):
        _objTranslate = QObject().tr
        _translate = QCoreApplication.translate
        init_obj_name = _objTranslate("MaterialNode")
        self.edit_file_path.settext(_translate(init_obj_name, _objTranslate("Texture File Path")))
        self.btn_browser.setText(_translate(init_obj_name, _objTranslate("BROWSE")))

    def _create_combo(self):
        colorspace = ["ARRI LogC", "camera Rec 709", "Sony SLog2", "Log film scam (ADX)", "Log-to-Lin (cineon)",
                      "Log-to-Lin (jzp)", "Raw", "ACES2065-1", "ACEScg", "scene-linear CIE XYZ", "scene-linear DCI-P3",
                      "scene-linear Rec 2020", "scene-linear Rec709/sRGB", "gamma 1.8 Rec 709", "gamma 2.2 Rec 709",
                      "gamma 2.4 Rec 709 (video)", "sRGB"]
        self.combo_colorspace.addItems(colorspace)


class MaterialManagerWidgets(QWidget):
    def __init__(self):
        super(MaterialManagerWidgets, self).__init__(parent=None)
        self.menu_bar = QMenuBar()
        self.viewer_geom = QListView()
        self.grp_box_materials = QGroupBox()
        self.btn_run = QPushButton()
        self.act_setting = QAction()

    def setup_widget(self, manager):
        manager.setObjectName("MaterialManagerWindow")
        layout = QVBoxLayout()
        box_layout = QHBoxLayout()
        self.menu_bar.addAction(self.act_setting)

        box_layout.addWidget(self.viewer_geom)
        box_layout.addWidget(self.grp_box_materials)
        layout.addWidget(self.menu_bar)
        layout.addLayout(box_layout)
        layout.addWidget(self.btn_run)

        self.setLayout(layout)
        self.retranslate_widget(manager)
        QMetaObject.connectSlotsByName(manager)

    def retranslate_widget(self, manager):
        _objTranslate = QObject().tr
        _translate = QCoreApplication.translate
        init_obj_name = _objTranslate("MaterialManagerWindow")
        manager.setWindowTitle(_translate(init_obj_name, _objTranslate("Material Manager")))
        self.act_setting.setText(_translate(init_obj_name, _objTranslate("Setting")))
        self.btn_run.setText(_translate(init_obj_name, _objTranslate("RUN")))