try:
	from PySide2 import QtWidgets, QtGui, QtCore
	from shiboken2 import wrapInstance
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	from shiboken6 import wrapInstance
	
from MSL_MayaRename.core.resources import Resources
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
	
	WINDOW_TITLE = "MSL Rename"

	def __init__(self, parent=maya_main_window()):
		super(MainToolWindow, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon = self.resources.get_icon_from_resources("earth-svgrepo-com.svg")
		self.has_state_cache = self.resources.config.get_variable("library", "show_cache", False, bool)
		self.window_geometry = self.resources.config.get_variable("startup", "window_geometry", QtCore.QRect(), QtCore.QRect)
		# Setting---------------------------
		if self.window_geometry:
			self.setGeometry(self.window_geometry)
			self.setFixedSize(self.window_geometry.width(), self.window_geometry.height())
		else:
			self.setFixedSize(305, 180)
		self.setWindowTitle(self.WINDOW_TITLE)
		self.setObjectName("MainRenameToolWindowID")
		self.setWindowIcon(self.icon)  # crab-svgrepo-com  pen-svgrepo-com earth-svgrepo-com
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

		
	def create_widgets(self):
		self.RenameGUI = RenameGUI()
		
	def create_layouts(self):
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)
		
		self.main_layout.addWidget(self.RenameGUI)
		
	def create_connections(self):
		self.RenameGUI.QuickListButtonName.itShowCahe.connect(self.show_cache)
		self.RenameGUI.LetterWidget.itShowLetter.connect(self.show_letter_mode)
		
	def show_cache(self, state):
		if state:
			widget_height = self.height() + 30
		else:
			widget_height = self.height() - 30
		self.setFixedHeight(widget_height)
		self.save_geometry()
		
	def show_letter_mode(self, state):
		if state:
			widget_height = self.height() + 25
		else:
			widget_height = self.height() - 25
		self.setFixedHeight(widget_height)
		self.save_geometry()
	
	def moveEvent(self, event: QtGui.QMoveEvent):
		super().moveEvent(event)

		
	def showEvent(self, e):
		self.RenameGUI.LabelWidget.set_script_job_enabled(True)

	def closeEvent(self, e):
		self.RenameGUI.LabelWidget.set_script_job_enabled(False)
		self.save_geometry()
		
	def save_geometry(self):
		self.resources.config.set_variable("startup", "window_geometry", self.geometry())
	
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			event.ignore()
		else:
			super().keyPressEvent(event)


def creat_gui():
	if cmds.window("MainRenameToolWindowID", exists=True):
		cmds.deleteUI("MainRenameToolWindowID")

	if cmds.windowPref("MainRenameToolWindowID", exists=1):
		cmds.windowPref("MainRenameToolWindowID", remove=1)
	
	try:
		win.close()  # pylint: disable=E0601
		win.deleteLater()
	except:
		pass

	win = MainToolWindow()
	win.show()