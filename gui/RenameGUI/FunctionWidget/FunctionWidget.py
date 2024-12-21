from os import rename

try:
    from PySide2 import QtWidgets, QtGui, QtCore, QtSvg
except:
    from PySide6 import QtWidgets, QtGui, QtCore, QtSvg

import os
import maya.cmds as cmds
from MSL_MayaRename.core.resources import Resources


class FunctionWidget(QtWidgets.QWidget):
    Style_btn = """
    	    QPushButton {
    	        background-color: rgb(50, 50, 50); /* Темно-серый фон */
    	        border-style: outset;
    	        border-width: 2px;
    	        border-radius: 8px;
    	        border-color: rgb(30, 30, 30); /* Темнее границы */
    	        font: normal 12px; /* Жирный шрифт */
    	        font-family: Roboto; /* Шрифт Arial  Helvetica, Calibri, Verdana, Tahoma, Segoe UI, Open Sans, Roboto, Source Sans Pro */
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
    	"""
    
    def __init__(self, parent=None):
        super(FunctionWidget, self).__init__(parent)
        
        # Modul---------------------------
        self.resources = Resources.get_instance()
        # Attribute---------------------------
        self.FixedHeight = 25
        # Setting---------------------------
        self.setObjectName("FunctionWidgetID")
        self.setFixedHeight(self.FixedHeight)
        self.setStyleSheet(self.Style_btn)
        # Run functions ---------------------------
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # button AA --> NANE - upper
        self.AA_BTN = QtWidgets.QPushButton("AA")
        self.AA_BTN.setFixedSize(25, 25)
        # button Aa --> Name - capitalize
        self.Aa_BTN = QtWidgets.QPushButton("Aa")
        self.Aa_BTN.setFixedSize(25, 25)
        # button aa --> Name - lower
        self.aa_BTN = QtWidgets.QPushButton("aa")
        self.aa_BTN.setFixedSize(25, 25)
        # button AP - auto prefix --> lt_Name rt_Name mid_Name
        self.AP_BTN = QtWidgets.QPushButton("AP")
        self.AP_BTN.setFixedSize(25, 25)

        # button RP remove pref_  --> pref_Name --> Name
        self.RP_BTN = QtWidgets.QPushButton("RP")
        self.RP_BTN.setFixedSize(25, 25)
        # button RS remove _suffix  --> Name_suffix --> Name
        self.RS_BTN = QtWidgets.QPushButton("RS")
        self.RS_BTN.setFixedSize(25, 25)
        # button DE delet end number --> Name01 --> Name
        self.DE_BTN = QtWidgets.QPushButton("DE")
        self.DE_BTN.setFixedSize(25, 25)
        # button DA delet all number --> 01Name01 --> Name
        self.DA_BTN = QtWidgets.QPushButton("DA")
        self.DA_BTN.setFixedSize(25, 25)

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_layout.addWidget(self.AA_BTN)
        self.main_layout.addWidget(self.Aa_BTN)
        self.main_layout.addWidget(self.aa_BTN)
        self.main_layout.addWidget(self.AP_BTN)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.RP_BTN)
        self.main_layout.addWidget(self.RS_BTN)
        self.main_layout.addWidget(self.DE_BTN)
        self.main_layout.addWidget(self.DA_BTN)

    def create_connections(self):
        self.AA_BTN.clicked.connect(lambda: self.rename_selected_objects_case(mode="upper"))
        self.Aa_BTN.clicked.connect(lambda: self.rename_selected_objects_case(mode="capitalize"))
        self.aa_BTN.clicked.connect(lambda: self.rename_selected_objects_case(mode="lower"))
    
    def rename_selected_objects_case(self, mode="capitalize"):
        """
        Changes the case of names of selected objects.
        """
        selection = cmds.ls(selection=True, l=True)
        filtered_list = self.parent().FindReplaceWidget.remove_shapes_from_transforms(selection)
        
        if filtered_list:
            for obj in filtered_list:
  
                path_to_obj, obj_short_name = self.parent().get_short_name(obj)
                if mode == "capitalize":
                    new_name = obj_short_name.capitalize()
                elif mode == "lower":
                    new_name = obj_short_name.lower()
                elif mode == "upper":
                    new_name = obj_short_name.upper()
                
                obj_rename = cmds.rename(obj, new_name)
                new_path_to_obj, new_obj_short_name = self.parent().get_short_name(obj_rename)
                new_obj = path_to_obj + new_obj_short_name
                
                filtered_list = self.parent().renameObjectsInHierarchy(filtered_list, obj, new_obj)
            
            self.parent().LabelWidget.update_selection()

        else:
            print("It is necessary to select an object.")