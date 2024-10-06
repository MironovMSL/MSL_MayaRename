try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.gui.RenameGUI.RenameWidget.LineEditorWidget import LineEditorWidget
from MSL_MayaRename.gui.RenameGUI.RenameWidget.RemoveButtonWidget import RemoveButtonWidget
import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class RenameWidget(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(RenameWidget, self).__init__(parent)
		# Attribute----------------------
		self.FixedHeight = 25

		# Setting ------------------------
		self.setFixedHeight(self.FixedHeight)

		# Run function ------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()

	def create_widgets(self):

		# create buttons
		self.LeftRemoveButton = RemoveButtonWidget("",25,25,"Right_chevron-arrows-svgrepo-com.svg","first")
		self.RightRemoveButton = RemoveButtonWidget("",25,25,"Left_chevron-arrows-svgrepo-com.svg","end")
		# create LineEditor
		self.LineEditor = LineEditorWidget()

	def create_layouts(self):

		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.main_layout.addWidget(self.LeftRemoveButton)
		self.main_layout.addWidget(self.LineEditor)
		self.main_layout.addWidget(self.RightRemoveButton)

	def create_connections(self):
		self.LeftRemoveButton.clicked.connect(self.click_on_remove_left)
		self.RightRemoveButton.clicked.connect(self.click_on_remove_right)

		# self.LineEditor.AutoComplete_line_edit.textChanged.connect(self.do_text_edited)

	def click_on_remove_left(self):
		print("TODO : remove the first letter")

	def click_on_remove_right(self):
		print("TODO : remove the edn letter")

	# def do_text_edited(self, text):
	# 	print(f"TODO :RenameWidget.py textChanged: {text}")
