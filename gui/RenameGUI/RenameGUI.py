try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.gui.RenameGUI.FunctionWidget.FunctionWidget import FunctionWidget
from MSL_MayaRename.gui.RenameGUI.RenameWidget.RenameWidget import RenameWidget
from MSL_MayaRename.gui.RenameGUI.NumberWidget.NumberWidget import NumberWidget
from MSL_MayaRename.gui.RenameGUI.LetterWidget.LetterWidget import LetterWidget
from MSL_MayaRename.gui.RenameGUI.SuffixPrefixWidget.SuffixPrefixWidget import SuffixPrefixWidget
from MSL_MayaRename.gui.RenameGUI.LabelWidget.LabelWidget import LabelWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonName.QuickListButtonName import QuickListButtonName
from MSL_MayaRename.gui.RenameGUI.CasheNameWidget.CasheNameWidget import CasheNameWidget

import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class RenameGUI(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(RenameGUI, self).__init__(parent)

		self.FixedHeigt = 200
		self.resources :Configurator = Resources.get_instance()

		self.setFixedHeight(self.FixedHeigt)

		self.create_Widgets()
		self.create_layouts()
		self.create_connections()

	def create_Widgets(self):

		self.FunctionWidget = FunctionWidget()
		self.LabelWidget = LabelWidget()
		self.RenameButton = QtWidgets.QPushButton("Rename")
		self.RenameButton.setFixedSize(50, 75)
		self.RenameWidget = RenameWidget()
		self.NumberWidget = NumberWidget()
		self.LetterWidget = LetterWidget()
		self.SuffixPrefixWidget = SuffixPrefixWidget()
		self.QuickListButtonName = QuickListButtonName()
		self.CasheNameWidget = CasheNameWidget()

	def create_layouts(self):
		# main layout
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# left and Right layout for widgets ---> RenameWidget, NumberWidget, LetterWidget,
		self.main_rename_layout = QtWidgets.QHBoxLayout()
		self.main_rename_layout.setContentsMargins(0, 0, 0, 0)
		self.main_rename_layout.setSpacing(0)

		self.left_layout = QtWidgets.QVBoxLayout()
		self.left_layout.setContentsMargins(0, 0, 0, 0)
		self.left_layout.setSpacing(0)
		self.Right_lyout = QtWidgets.QVBoxLayout()
		self.Right_lyout.setContentsMargins(0, 0, 0, 0)
		self.Right_lyout.setSpacing(0)

		self.main_rename_layout.addLayout(self.left_layout)
		self.main_rename_layout.addLayout(self.Right_lyout)

		# add LabelWidget RenameWidget, NumberWidget, LetterWidget, RenameButton, SuffixPrefixWidget, QuickListButtonName

		self.main_layout.addWidget(self.FunctionWidget)
		self.main_layout.addWidget(self.LabelWidget)
		self.main_layout.addLayout(self.main_rename_layout)
		self.left_layout.addWidget(self.RenameWidget)
		self.left_layout.addWidget(self.LetterWidget)
		self.left_layout.addWidget(self.NumberWidget)
		self.Right_lyout.addWidget(self.RenameButton)
		self.main_layout.addWidget(self.SuffixPrefixWidget)
		self.main_layout.addWidget(self.QuickListButtonName)
		self.main_layout.addWidget(self.CasheNameWidget)

		self.main_layout.addStretch()

	def create_connections(self):
		pass


