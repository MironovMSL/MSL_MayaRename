try:
    from PySide2 import QtWidgets, QtGui, QtCore, QtSvg
except:
    from PySide6 import QtWidgets, QtGui, QtCore, QtSvg

import os
import maya.cmds as cmds
from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.FunctionWidget.CustomPushButton import CustomPushButton
import re


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
        self.AA_BTN = CustomPushButton("AA")
        self.AA_BTN.setToolTip("Text converted to Upper.")
        # button Aa --> Name - capitalize
        self.Aa_BTN = CustomPushButton("Aa")
        self.Aa_BTN.setToolTip("Text converted to Capitalize.")
        # button aa --> Name - lower
        self.aa_BTN = CustomPushButton("aa")
        self.aa_BTN.setToolTip("Text converted to Lower.")
        # button RP remove pref_  --> pref_Name --> Name
        self.RP_BTN = CustomPushButton("A_")
        self.RP_BTN.setToolTip("Remove prefix in name.")
        # button RS remove _suffix  --> Name_suffix --> Name
        self.RS_BTN = CustomPushButton("_A")
        self.RS_BTN.setToolTip("Remove suffix in name.")
        # button DT remove trail number --> Name01 --> Name
        self.DE_BTN = CustomPushButton("_1")
        self.DE_BTN.setToolTip("Remove the numerical tail.")
        # button DA remove all number --> 01Name01 --> Name
        self.DA_BTN = CustomPushButton("1_1")
        self.DA_BTN.setToolTip("Remove all numbers.")

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.main_layout.addWidget(self.AA_BTN)
        self.main_layout.addWidget(self.Aa_BTN)
        self.main_layout.addWidget(self.aa_BTN)
        self.main_layout.addWidget(self.RP_BTN)
        self.main_layout.addWidget(self.RS_BTN)
        self.main_layout.addWidget(self.DE_BTN)
        self.main_layout.addWidget(self.DA_BTN)
        # self.main_layout.addStretch()

    def create_connections(self):
        self.AA_BTN.clicked.connect(lambda: self.rename_selected_objects_case(mode="upper"))
        self.Aa_BTN.clicked.connect(lambda: self.rename_selected_objects_case(mode="capitalize"))
        self.aa_BTN.clicked.connect(lambda: self.rename_selected_objects_case(mode="lower"))
        self.RP_BTN.clicked.connect(lambda: self.rename_selected_objects_case(mode="remove_prefix"))
        self.RS_BTN.clicked.connect(lambda: self.rename_selected_objects_case(mode="remove_suffix"))
        self.DE_BTN.clicked.connect(lambda: self.rename_selected_objects_case(mode="remove_trailing_numbers"))
        self.DA_BTN.clicked.connect(lambda: self.rename_selected_objects_case(mode="remove_all_numbers"))
    
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
                elif mode == "remove_prefix":
                    new_name = self.remove_prefix(obj_short_name)
                elif mode == "remove_suffix":
                    new_name = self.remove_suffix(obj_short_name)
                elif mode == "remove_trailing_numbers":
                    new_name = self.remove_trailing_numbers(obj_short_name)
                elif mode == "remove_all_numbers":
                    new_name = self.remove_all_numbers(obj_short_name)
                
                obj_rename = cmds.rename(obj, new_name)
                new_path_to_obj, new_obj_short_name = self.parent().get_short_name(obj_rename)
                new_obj = path_to_obj + new_obj_short_name
                
                filtered_list = self.parent().renameObjectsInHierarchy(filtered_list, obj, new_obj)
            
            self.parent().LabelWidget.update_selection()

        else:
            print("It is necessary to select an object.")
            
    def remove_prefix(self, name):
        parts = name.split("_")

        if len(parts) == 1:
            new_name = name
        else:
            new_name = "_".join(parts[1:])
            
        return new_name
    
    def remove_suffix(self, name):
        parts = name.rsplit("_", 1)
        
        if len(parts) == 1:
            new_name = name
        else:
            new_name = parts[0]
            
        return  new_name
    
    def remove_trailing_numbers(self, name):
        new_name = re.sub(r'_?\d+$', '', name).rstrip('_')
        return  new_name
    
    def remove_all_numbers(self, name):
        new_name = re.sub(r'\d+', '', name).rstrip('_')
        new_name = re.sub(r'__+', '_', new_name)
        return new_name
        