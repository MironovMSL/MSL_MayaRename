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
        pass
    
    def show_find_replace(self, state):
        self.state_find_replace = state
        self.setVisible(state)
        
        self.itShowFindReplace.emit(state)