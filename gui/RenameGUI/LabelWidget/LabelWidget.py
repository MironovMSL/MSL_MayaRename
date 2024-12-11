try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore

from functools import partial

from MSL_MayaRename.gui.RenameGUI.LabelWidget.NumberModeButton import NumberModeButton
from MSL_MayaRename.gui.RenameGUI.LabelWidget.PushButtonModeBTN import PushButtonModeBTN
from MSL_MayaRename.gui.RenameGUI.LabelWidget.CustomeLabelWidget import CustomeLabelWidget
from MSL_MayaRename.gui.RenameGUI.LabelWidget.FindReplaceModeButton import FindReplaceModeButton
from MSL_MayaRename.gui.RenameGUI.LabelWidget.SelectedObjectsViewerButton import SelectedObjectsViewerButton

import maya.cmds as cmds

class LabelWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(LabelWidget, self).__init__(parent)

        # Attribute ---------------------------
        self.FixedHeight = 25
        self.script_job_number = -1
        # Setting ---------------------------
        self.setObjectName("LabelWidgetID")
        self.setFixedHeight(self.FixedHeight)
        # Run functions ---------------------------
        self.create_Widgets()
        self.create_layouts()
        self.create_connections()
        self.update_selection()

    def create_Widgets(self):
        # button list ---------------------------
        self.list_selected_btn = SelectedObjectsViewerButton("0", 25, 25)
        # label ---------------------------
        self.label_name        = CustomeLabelWidget()
        # namber mode ---------------------------
        self.number_mode       = NumberModeButton("",25, 25,)
        # button mode ---------------------------
        self.button_mode       = PushButtonModeBTN("", 25, 25)
        # find_relace mode ---------------------------
        self.find_replace_mode = FindReplaceModeButton()

    def create_layouts(self):
        # main layout---------------------------
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        # add widget---------------------------
        self.main_layout.addWidget(self.list_selected_btn)
        self.main_layout.addWidget(self.label_name)
        self.main_layout.addWidget(self.number_mode)
        self.main_layout.addWidget(self.button_mode)
        self.main_layout.addWidget(self.find_replace_mode)

    def create_connections(self):
        pass

    def update_selection(self):
        """
        Updates the current selection of objects in the scene and reflects this in the UI.
        """
        selection = cmds.ls(selection=True,  l=True)

        self.label_name.update_selection(selection)
        self.list_selected_btn.setText(str(len(selection)))
        #TODO: creat UI selected objects and give list.

    def set_script_job_enabled(self, enabled):
        """
        Enables or disables a script job that monitors selection changes in the Maya scene.
        """
        if enabled and self.script_job_number < 0:
            self.script_job_number = cmds.scriptJob(event=["SelectionChanged", partial(self.update_selection)],
                                                    protected=True)
        elif not enabled and self.script_job_number >= 0:
            cmds.scriptJob(kill=self.script_job_number, force=True)
            self.script_job_number = -1
