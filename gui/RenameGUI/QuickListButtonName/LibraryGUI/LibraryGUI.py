try:
	from PySide2 import QtWidgets, QtGui, QtCore
	from shiboken2 import wrapInstance
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	from shiboken6 import wrapInstance
	
from MSL_MayaRename.core.resources import Resources
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import sys


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class LibraryWindow(QtWidgets.QDialog):
	WINDOW_TITLE = "Library Rename Tool"
	library_show = QtCore.Signal(bool)
	
	def __init__(self, parent=maya_main_window()):
		super(LibraryWindow, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon = self.resources.get_icon_from_resources("earth-svgrepo-com.svg")
		# Setting---------------------------
		self.setWindowTitle(self.WINDOW_TITLE)
		self.setObjectName("LibraryWindowRenameToolWindowID")
		self.setWindowIcon(self.icon)
		self.setMinimumSize(180, 200)
		self.setMaximumSize(420, 350)
		self.resize(300, 350)
		
		# On macOS make the window a Tool to keep it on top of Maya
		if sys.platform == "darwin":
			self.setWindowFlag(QtCore.Qt.Tool, True)
		
		# Remove Title
		# self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
		# self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
	
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
		
	def __repr__(self):
		return f"Class: [LibraryWindow], name = [{self.objectName()}]"
	
	def create_widgets(self):
		FixedHeigt = 25
		
		self.conten = QtWidgets.QWidget()
		self.conten.setStyleSheet("background-color: #555555; border-radius: 10px;")
		self.conten.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.conten.setFixedHeight(25)
		
		self.conten2 = QtWidgets.QWidget()
		self.conten2.setStyleSheet("background-color: #555580; border-radius: 10px;")
		self.conten2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.conten2.setFixedHeight(250)
		
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
	
	def create_layouts(self):
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)
		
		self.main_layout.addWidget(self.conten)
		self.main_layout.addWidget(self.conten2)
		self.main_layout.addWidget(self.conten3)
		self.main_layout.addWidget(self.conten4)
		self.main_layout.addWidget(self.conten5)
	
	def create_connections(self):
		pass
	
	def closeEvent(self, event):
		self.library_show.emit(False)
		