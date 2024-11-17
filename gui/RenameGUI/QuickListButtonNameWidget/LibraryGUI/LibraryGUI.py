try:
	from PySide2 import QtWidgets, QtGui, QtCore
	from shiboken2 import wrapInstance
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	from shiboken6 import wrapInstance
	
from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.LibraryScrollAreaWidget.MainScrollAreaLibraryWidget import MainScrollAreaLibraryWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.AdditionButtonsWidget import AdditionButtonsWidget
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import sys


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class LibraryWindow(QtWidgets.QDialog):
	WINDOW_TITLE = "Library"
	library_show = QtCore.Signal(bool)
	
	def __init__(self, parent=maya_main_window()):
		super(LibraryWindow, self).__init__(parent)
		# Modul---------------------------
		self.resources   = Resources.get_instance()
		# Attribute---------------------------
		self.icon        = self.resources.get_icon_from_resources("earth-svgrepo-com.svg")
		self.step_width  = 60
		self.step_height = 20
		self.target_size = None
		self.resize_anim = None
		# Setting---------------------------
		self.setWindowTitle(self.WINDOW_TITLE)
		self.setObjectName("LibraryWindowRenameToolWindowID")
		self.setWindowIcon(self.icon)
		self.setMinimumSize(240, 200)
		self.setMaximumSize(420, 355)
		self.resize(300, 355)
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
		return f"Class: [LibraryWindow], name - [{self.objectName()}]"
	
	def create_widgets(self):
		self.resize_timer = QtCore.QTimer()
		self.resize_timer.setSingleShot(True)
		
		self.MainScrollArea = MainScrollAreaLibraryWidget()
		self.AdditionButtonsWidget = AdditionButtonsWidget()
		
		self.conten = QtWidgets.QWidget()
		self.conten.setStyleSheet("background-color: #D17535; border-radius: 10px;")
		self.conten.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.conten.setFixedHeight(25)

	def create_layouts(self):
		# main layout---------------------------
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)
		# add widget---------------------------
		self.main_layout.addWidget(self.conten)
		self.main_layout.addWidget(self.MainScrollArea)
		self.main_layout.addWidget(self.AdditionButtonsWidget)
	
	def create_connections(self):
		self.resize_timer.timeout.connect(self.applyStepResize)
	
	def closeEvent(self, event):
		self.library_show.emit(False)
	
	def resizeEvent(self, event):
		if self.resize_anim:
			if self.resize_anim.state() == QtCore.QAbstractAnimation.Running:
				return
		width = event.size().width()
		height = event.size().height()
		
		# Round the width and height to the nearest step
		new_width = (width // self.step_width) * self.step_width
		new_height = ((height - 15) // self.step_height) * self.step_height + (15)
		
		# Check if the size needs to be increased or decreased
		width_diff = width - new_width
		height_diff = height - new_height
		
		if width_diff > self.step_width / 2:
			new_width += self.step_width
		elif width_diff < -self.step_width / 2:
			new_width -= self.step_width
		
		if height_diff > self.step_height / 2:
			new_height += self.step_height
		elif height_diff < -self.step_height / 2:
			new_height -= self.step_height
		
		# Set the target size
		self.target_size = QtCore.QSize(new_width, new_height)
		
		self.resize_timer.start(300)
		super().resizeEvent(event)
	
	def applyStepResize(self):
		# self.resize(self.target_size)
		start_size = self.size()
		
		self.resize_anim = QtCore.QPropertyAnimation(self, b"size")
		self.resize_anim.setStartValue(start_size)
		self.resize_anim.setEndValue(self.target_size)
		self.resize_anim.setDuration(100)
		self.resize_anim.start()
		
		