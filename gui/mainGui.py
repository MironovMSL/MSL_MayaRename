try:
	from PySide2 import QtWidgets, QtGui, QtCore
	from shiboken2 import wrapInstance
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	from shiboken6 import wrapInstance

import sys
import os
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from MSL_MayaRename.gui.RenameGUI.RenameGUI import RenameGUI

root_ = os.path.dirname(__file__)

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MainToolWindow(QtWidgets.QDialog):

	def __init__(self, parent=maya_main_window()):
		super().__init__(parent)

		self.setWindowTitle("MSL Rename")
		self.setObjectName("MainToolWindowID")
		self.setWindowIcon(QtGui.QIcon(os.path.join(root_,"resources", "icon", "earth-svgrepo-com.svg")))  # crab-svgrepo-com  pen-svgrepo-com earth-svgrepo-com
		self.setMinimumWidth(300)
		self.setMinimumHeight(250)

		# On macOS make the window a Tool to keep it on top of Maya
		if sys.platform == "darwin":
			self.setWindowFlag(QtCore.Qt.Tool, True)

		# Remove Title
		# self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
		# self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		# main layout
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)
		# self.setFixedSize(300, 250)

		# content
		FixedHeigt = 25


		self.RenameGUI = RenameGUI()

		self.conten = QtWidgets.QWidget()
		self.conten.setStyleSheet("background-color: #555555; border-radius: 10px;")
		self.conten.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.conten.setFixedHeight(FixedHeigt)

		self.conten2 = QtWidgets.QWidget()
		self.conten2.setStyleSheet("background-color: #555580; border-radius: 10px;")
		self.conten2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.conten2.setFixedHeight(FixedHeigt)

		self.conten3 = QtWidgets.QWidget()
		self.conten3.setStyleSheet("background-color: #955890; border-radius: 10px;")
		self.conten3.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.conten3.setFixedHeight(FixedHeigt)

		self.conten4 = QtWidgets.QWidget()
		self.conten4.setStyleSheet("background-color: #55aaff; border-radius: 10px;")
		self.conten4.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.conten4.setFixedHeight(FixedHeigt)

		self.conten5 = QtWidgets.QWidget()
		self.conten5.setStyleSheet("background-color: #ffaa7f; border-radius: 10px;")
		self.conten5.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.conten5.setFixedHeight(FixedHeigt)



		# self.main_layout.addWidget(self.conten)
		self.main_layout.addWidget(self.RenameGUI)
		self.main_layout.addWidget(self.conten2)
		self.main_layout.addWidget(self.conten3)
		# # self.main_layout.addWidget(self.conten4)
		# # self.main_layout.addWidget(self.conten5)

def creat_gui():
	if cmds.window("MainToolWindowID", exists=True):
		cmds.deleteUI("MainToolWindowID")

	win = MainToolWindow()
	win.show()