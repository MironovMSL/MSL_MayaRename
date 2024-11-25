try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.common import *
from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryButtonMode import LibraryButtonMode
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.CustomScrollArea import CustomScrollArea
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.СacheWidget.CacheWidget import CacheWidget

import os
import maya.cmds as cmds

class QuickListButtonNameWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(QuickListButtonNameWidget, self).__init__(parent)

        # Attribute---------------------------
        self.FixedHeight = 60
        # Setting---------------------------
        self.setObjectName("QuickListButtonNameID")
        self.setFixedHeight(self.FixedHeight)
        # Run functions ---------------------------
        self.create_Widgets()
        self.create_layouts()
        self.create_connections()

    def create_Widgets(self):
        self.library_BTN = LibraryButtonMode(25, 25)
        self.Scroll_Area = CustomScrollArea()
        self.cache_area  = CacheWidget()

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.QuickButtonlayount = QtWidgets.QHBoxLayout(self)
        self.QuickButtonlayount.setContentsMargins(0, 0, 0, 0)
        self.QuickButtonlayount.setSpacing(0)

        self.QuickButtonlayount.addWidget(self.Scroll_Area)
        self.QuickButtonlayount.addWidget(self.library_BTN)
        
        self.main_layout.addLayout(self.QuickButtonlayount)
        self.main_layout.addWidget(self.cache_area)


    def create_connections(self):
        pass