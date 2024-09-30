try:
    from PySide2 import QtWidgets, QtGui, QtCore, QtSvg
except:
    from PySide6 import QtWidgets, QtGui, QtCore, QtSvg

import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__) #...\LabelWidget
new_root = os.path.abspath(os.path.join(root_, '..', '..')) # ...\gui

class LabelWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LabelWidget, self).__init__(parent)

        self.setObjectName("LabelWidget")

        self.FixedHeight = 25
        self.name_label_empty = "  selected"
        self.SuffixHolder = "_suffix"

        self.setFixedHeight(self.FixedHeight)


        self.create_Widgets()
        self.create_layouts()
        self.create_connections()

    def create_Widgets(self):

        Width = 90
        # button add prefix
        self.list_selected_btn = QtWidgets.QPushButton("0")
        self.list_selected_btn.setFixedWidth(25)

        # label
        self.label_name = QtWidgets.QLabel(self.name_label_empty)

        # button mode
        self.number_mode = QtWidgets.QPushButton("01")
        self.number_mode.setFixedWidth(25)

        self.button_mode = QtWidgets.QPushButton("AP")
        self.button_mode.setFixedWidth(25)


    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_layout.addWidget(self.list_selected_btn)
        self.main_layout.addWidget(self.label_name)
        self.main_layout.addWidget(self.number_mode)
        self.main_layout.addWidget(self.button_mode)


    def create_connections(self):
        pass