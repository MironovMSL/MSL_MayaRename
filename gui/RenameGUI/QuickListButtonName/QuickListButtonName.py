try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.common import *
from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonName.LibraryButtonMode import LibraryButtonMode
from MSL_MayaRename.gui.RenameGUI.QuickListButtonName.CustomButtonLibrary import CustomButtonLibrary

import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__) #...\QuickListButtonName
new_root = os.path.abspath(os.path.join(root_, '..', '..')) # ...\gui

class QuickListButtonName(QtWidgets.QWidget):

    Style_btn = """
    	        QPushButton {
    	            background-color: rgb(50, 50, 50); /* Темно-серый фон */
    	            border-style: outset;
    	            border-width: 2px;
    	            border-radius: 8px;
    	            border-color: rgb(30, 30, 30); /* Темнее границы */
    	            font: bold 14px; /* Жирный шрифт */
    	            font-family: Arial; /* Шрифт Arial */
    	            color: rgb(200, 200, 200); /* Светло-серый текст */
    	            padding: 0px; /* Внутренние отступы */
    	        }

    	        QPushButton:hover {
    	            border-color: rgb(70, 70, 70); /* Светло-серая граница при наведении */
    	            background-color: rgb(80, 80, 80); /* Более светлый серый при наведении */
    	        }

    	        QPushButton:pressed {
    	            background-color: rgb(30, 30, 30); /* Почти черный при нажатии */
    	            border-style: inset; /* Впадение при нажатии */
    	            color: rgb(220, 220, 220); /* Почти белый текст при нажатии */
    	        }

    	        QPushButton:checked {
    	            background-color: rgb(80, 120, 80); /* Зеленоватый оттенок при нажатии (состояние check) */
    	            border-color: rgb(60, 90, 60); /* Темно-зеленая граница при нажатии */
    	            color: rgb(240, 240, 240); /* Белый текст */
    	        }

    	        QPushButton:checked:hover {
    	            background-color: rgb(100, 140, 100); /* Светлее при наведении в состоянии checked */
    	            border-color: rgb(80, 110, 80); /* Светлее при наведении в состоянии checked */
    	        }
    	    """

    def __init__(self, parent=None):
        super(QuickListButtonName, self).__init__(parent)

        # Attribute---------------------------
        self.FixedHeight = 25
        # Setting---------------------------
        self.setObjectName("QuickListButtonNameID")
        self.setFixedHeight(self.FixedHeight)
        # self.setStyleSheet(self.Style_btn)
        # Run functions ---------------------------
        self.create_Widgets()
        self.create_layouts()
        self.create_connections()

    def create_Widgets(self):
        self.library_BTN = LibraryButtonMode(25, 25)

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        list_BTN = get_list_itemJSON("fast_access")
        for i in list_BTN:
            self.btn = CustomButtonLibrary(i, 40,25)
            self.main_layout.addWidget(self.btn)


        self.main_layout.addStretch()
        self.main_layout.addWidget(self.library_BTN)


    def create_connections(self):
        pass