try:
    from PySide2 import QtWidgets, QtGui, QtCore, QtSvg
except:
    from PySide6 import QtWidgets, QtGui, QtCore, QtSvg

from MSL_MayaRename.gui.RenameGUI.FindReplaceWidget.FindBytton import FindBytton
from MSL_MayaRename.gui.RenameGUI.FindReplaceWidget.ReplaceBytton import ReplaceBytton
from MSL_MayaRename.gui.RenameGUI.FindReplaceWidget.LineEditorWidget import LineEditorWidget
from MSL_MayaRename.gui.RenameGUI.FindReplaceWidget.TypeFindButton import TypeFindButton

from MSL_MayaRename.core.resources import Resources
import maya.cmds as cmds


class FindReplaceWidget(QtWidgets.QWidget):
    itShowFindReplace = QtCore.Signal(bool)
    
    def __init__(self, parent=None):
        super(FindReplaceWidget, self).__init__(parent)
        # Module----------------------
        self.resources = Resources.get_instance()
        # Attribute----------------------
        self.state_find_replace = self.resources.config.get_variable("startup", "mode_find_replace", False, bool)
        self.FixedHeight  = 25
        # Setting ------------------------
        self.setObjectName("FindReplaceWidgetID")
        self.setFixedHeight(self.FixedHeight)
        if not self.state_find_replace:
            self.setVisible(self.state_find_replace)
        # Run function ------------------------
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        Width = 120
        self.find_btn         = FindBytton()
        self.find_editline    = LineEditorWidget("Search", Width)
        self.type_find_btn    = TypeFindButton()
        self.replace_editline = LineEditorWidget("Replace", Width)
        self.replace_btn      = ReplaceBytton()

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_layout.addWidget(self.find_btn)
        self.main_layout.addWidget(self.find_editline)
        self.main_layout.addWidget(self.type_find_btn)
        self.main_layout.addWidget(self.replace_editline)
        self.main_layout.addWidget(self.replace_btn)

    def create_connections(self):
        self.find_btn.clicked.connect(self.Search_objects)
        self.replace_btn.clicked.connect(self.Replace_objects)
    
    def show_find_replace(self, state):
        self.state_find_replace = state
        self.setVisible(state)
        
        self.itShowFindReplace.emit(state)
    
    def Replace_objects(self):
        """Replaces text in the names of selected objects"""
        replace_name = self.validate_input(self.replace_editline.AutoComplete_line_edit, "Replace")
        search_name, list_obj = self.Search_objects()

        if not list_obj:
            return

        if replace_name and search_name:
            sorted_objects = sorted(list_obj, key=len, reverse=True)
            for obj in sorted_objects:
                obj_short_name = self.parent().get_short_name(obj)[1]
                new_name = obj_short_name.replace(search_name, replace_name, 1)
                cmds.rename(obj, new_name)

        # Update the selection in the UI
        self.parent().LabelWidget.update_selection()
    
    def Search_objects(self):
        """Searches for objects by text in their names"""
        search_name = self.validate_input(self.find_editline.AutoComplete_line_edit, "Search")
        list_obj    = self.get_list_objects()
        list_matching_objects = [ ]
        
        if not list_obj:
            print("It is necessary to select an object.")
            return search_name, list_matching_objects
        
        if search_name:
            list_matching_objects = [
                obj for obj in list_obj if search_name in self.parent().get_short_name(obj)[1]
            ]
            cmds.select(list_matching_objects)
            
        filtered_list = self.remove_shapes_from_transforms(list_matching_objects)
        
        return search_name, filtered_list
        
    def get_list_objects(self):
        selection_type  = self.type_find_btn.type
        
        if selection_type  == "selected":
            list_obj = cmds.ls(sl=1, l=1) or []
        elif selection_type  == "hierarchy":
            selected  = cmds.ls(sl=1, l=1) or []
            hierarchy = cmds.ls(sl=1, dag=1, l=1) or []
            list_obj  = list(dict.fromkeys(selected + hierarchy))
        elif selection_type  == "all":
            list_obj = cmds.ls() or []
            
        return list_obj
    
    def validate_input(self, field, field_name):
        """Validates a text input field"""
        text = field.text()
        if not text:
            print(f"The {field_name} input field is empty. Please enter some text.")
        return text
    
    def remove_shapes_from_transforms(self, object_list):
        filtered_list = []

        for obj in object_list:
            if not cmds.objectType(obj, isType="transform"):
                parent_transform = cmds.listRelatives(obj, parent=True, fullPath=True)
                if parent_transform and parent_transform[0] in object_list:
                    continue
            
            filtered_list.append(obj)
        
        return filtered_list
    