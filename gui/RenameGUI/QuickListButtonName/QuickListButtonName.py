try:
    from PySide2 import QtWidgets, QtGui, QtCore, QtSvg
except:
    from PySide6 import QtWidgets, QtGui, QtCore, QtSvg

from MSL_MayaRename.core.common import *

import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__) #...\QuickListButtonName
new_root = os.path.abspath(os.path.join(root_, '..', '..')) # ...\gui

class QuickListButtonName(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QuickListButtonName, self).__init__(parent)

        self.FixedHeight = 25

        self.setObjectName("QuickListButtonName")
        self.setFixedHeight(self.FixedHeight)

        self.create_Widgets()
        self.create_layouts()
        self.create_connections()

    def create_Widgets(self):
        self.library_BTN = QtWidgets.QPushButton()
        self.library_BTN.setIcon(QtGui.QIcon(os.path.join(new_root, "resources", "icon","pen-svgrepo-com.svg")))


    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        list_BTN = get_list_itemJSON("fast_access")
        for i in list_BTN:
            self.fast_access_BTN = QtWidgets.QPushButton(i)
            self.fast_access_BTN.setMaximumSize(40, 25)
            self.main_layout.addWidget(self.fast_access_BTN)

        self.main_layout.addStretch()
        self.main_layout.addWidget(self.library_BTN)


    def create_connections(self):
        pass