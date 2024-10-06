try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.gui.RenameGUI.LabelWidget.NumberModeButton import NumberModeButton
import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__) #...\LabelWidget
new_root = os.path.abspath(os.path.join(root_, '..', '..')) # ...\gui

class LabelWidget(QtWidgets.QWidget):
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
        super(LabelWidget, self).__init__(parent)

        self.resoures = Resources.get_instance()


        self.FixedHeight = 25
        self.name_label_empty = '<font color="red">selected</font> and <font color="blue">object</font>.'

        self.setObjectName("LabelWidget")
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
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)

        # namber mode
        self.number_mode = NumberModeButton("",25,25,)
        # button mode
        self.button_mode = QtWidgets.QPushButton("B")
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