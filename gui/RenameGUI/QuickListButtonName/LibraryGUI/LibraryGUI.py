try:
	from PySide2 import QtWidgets, QtGui, QtCore
	from shiboken2 import wrapInstance
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	from shiboken6 import wrapInstance
	
from MSL_MayaRename.core.resources import Resources
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class LibraryWindow(QtWidgets.QDialog):
	WINDOW_TITLE = "Library Rename Tool"
	library_show = QtCore.Signal(bool)
	
	def __init__(self, parent=maya_main_window()):
		super(LibraryWindow, self).__init__(parent)
		
		self.resources = Resources.get_instance()
		self.icon = self.resources.get_icon_from_resources("earth-svgrepo-com.svg")
		
		self.setWindowTitle(self.WINDOW_TITLE)
		self.setObjectName("LibraryWindowRenameToolWindowID")
		self.setWindowIcon(self.icon)
		self.setMinimumSize(180, 200)
		self.setMaximumSize(420, 350)
		self.resize(300, 210)
		
		# Remove Title
		# self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
		# self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
	def __repr__(self):
		return f"Class: [LibraryWindow], name = [{self.objectName()}]"
	
	def closeEvent(self, event):
		self.library_show.emit(False)
		