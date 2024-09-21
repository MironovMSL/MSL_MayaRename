try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.gui.RenameGUI.RenameWidget.LineEditorWidget import LineEditorWidget
import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class RenameGUI(QtWidgets.QWidget):
	def __init__(self, parent=None, FixedHeigt=25):
		super(RenameGUI, self).__init__(parent)

		self.FixedHeigt = FixedHeigt

		self.setFixedHeight(self.FixedHeigt)

		# main layout
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# content


		self.conten = QtWidgets.QWidget()
		self.conten.setStyleSheet("background-color: #555555; border-radius: 10px;")
		self.conten.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		# self.conten.setFixedHeight(self.FixedHeigt)

		self.conten2 = LineEditorWidget()
		# self.conten2.setStyleSheet("background-color: #555580; border-radius: 10px;")
		self.conten2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		# self.conten2.setFixedHeight(self.FixedHeigt)

		self.conten3 = QtWidgets.QWidget()
		self.conten3.setStyleSheet("background-color: #955890; border-radius: 10px;")
		self.conten3.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		# self.conten3.setFixedHeight(self.FixedHeigt)

		self.conten4 = QtWidgets.QWidget()
		self.conten4.setStyleSheet("background-color: #55aaff; border-radius: 10px;")
		self.conten4.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		# self.conten4.setFixedHeight(self.FixedHeigt)

		self.conten5 = QtWidgets.QWidget()
		self.conten5.setStyleSheet("background-color: #ffaa7f; border-radius: 10px;")
		self.conten5.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		# self.conten5.setFixedHeight(self.FixedHeigt)

		self.main_layout.addWidget(self.conten)
		self.main_layout.addWidget(self.conten2)
		self.main_layout.addWidget(self.conten3)
		self.main_layout.addWidget(self.conten4)
		self.main_layout.addWidget(self.conten5)
