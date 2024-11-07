try:
    from PySide2 import QtWidgets, QtGui, QtCore, QtSvg
except:
    from PySide6 import QtWidgets, QtGui, QtCore, QtSvg

from MSL_MayaRename.core.common import *

import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__) #...\CasheNameWidget
new_root = os.path.abspath(os.path.join(root_, '..', '..')) # ...\gui

class CasheNameWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CasheNameWidget, self).__init__(parent)

        self.FixedHeight = 25

        self.setObjectName("QuickListButtonNameWidget")
        self.setFixedHeight(self.FixedHeight)

        self.create_Widgets()
        self.create_layouts()
        self.create_connections()

    def create_Widgets(self):
        self.library_BTN = QtWidgets.QPushButton()
        self.library_BTN.setIcon(get_icon_from_resources("wind-energy-svgrepo-com.svg"))


    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # list_BTN = get_list_itemJSON("fast_access")
        for i in range(7):
            self.fast_access_BTN = QtWidgets.QPushButton(str(i))
            self.fast_access_BTN.setMaximumSize(40, 25)
            self.main_layout.addWidget(self.fast_access_BTN)
            self.fast_access_BTN.setIcon(get_icon_from_resources("sweep-the-floor-svgrepo-com.svg"))

        self.main_layout.addStretch()
        self.main_layout.addWidget(self.library_BTN)


    def create_connections(self):
        pass