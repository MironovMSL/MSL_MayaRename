try:
    from PySide2 import QtWidgets, QtGui, QtCore, QtSvg
except:
    from PySide6 import QtWidgets, QtGui, QtCore, QtSvg

import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__) #...\FunctionWidget
new_root = os.path.abspath(os.path.join(root_, '..', '..')) # ...\gui

class FunctionWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FunctionWidget, self).__init__(parent)

        self.FixedHeight = 25

        self.setObjectName("FunctionWidget")
        self.setFixedHeight(self.FixedHeight)


        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        # button AA --> NANE
        self.AA_BTN = QtWidgets.QPushButton("AA")
        self.AA_BTN.setFixedWidth(25)

        # button Aa --> Name
        self.Aa_BTN = QtWidgets.QPushButton("Aa")
        self.Aa_BTN.setFixedWidth(25)

        # button aa --> Name
        self.aa_BTN = QtWidgets.QPushButton("aa")
        self.aa_BTN.setFixedWidth(25)

        # # button AS - auto Suffix --> Name_geo
        # self.AS_BTN = QtWidgets.QPushButton("AS")
        # self.AS_BTN.setFixedWidth(25)

        # button AP - auto prefix --> lt_Name rt_Name mid_Name
        self.AP_BTN = QtWidgets.QPushButton("AP")
        self.AP_BTN.setFixedWidth(25)

        # button RP remove pref_  --> pref_Name --> Name
        self.RP_BTN = QtWidgets.QPushButton("RP")
        self.RP_BTN.setFixedWidth(25)

        # button RS remove _suffix  --> Name_suffix --> Name
        self.RS_BTN = QtWidgets.QPushButton("RS")
        self.RS_BTN.setFixedWidth(25)

        # button DE delet end number --> Name01 --> Name
        self.DE_BTN = QtWidgets.QPushButton("DE")
        self.DE_BTN.setFixedWidth(25)

        # button DA delet all number --> 01Name01 --> Name
        self.DA_BTN = QtWidgets.QPushButton("DA")
        self.DA_BTN.setFixedWidth(25)





    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_layout.addWidget(self.AA_BTN)
        self.main_layout.addWidget(self.Aa_BTN)
        self.main_layout.addWidget(self.aa_BTN)
        # self.main_layout.addWidget(self.AS_BTN)
        self.main_layout.addWidget(self.AP_BTN)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.RP_BTN)
        self.main_layout.addWidget(self.RS_BTN)
        self.main_layout.addWidget(self.DE_BTN)
        self.main_layout.addWidget(self.DA_BTN)


    def create_connections(self):
        pass