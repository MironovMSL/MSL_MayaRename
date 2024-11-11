try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.addCategoryButtonWidget import addCategoryButtonWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.addCategoryWidget import addCategoryWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.addSubCategoryButtonWidget import addSubCategoryButtonWidget

class AdditionButtonsWidget(QtWidgets.QWidget):

	def __init__(self, parent=None, ):
		super(AdditionButtonsWidget, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self._height = 25
		# Setting---------------------------
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.setFixedHeight(25)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	def create_widgets(self):
		self.addCategory = addCategoryButtonWidget()
		self.addSubCategory = addSubCategoryButtonWidget()
		self.addCategoryWidget = addCategoryWidget()
	

	def create_layouts(self):
		pass
		# main layout---------------------------
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		# self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
		# add widget---------------------------
		self.main_layout.addWidget(self.addCategory)
		self.main_layout.addWidget(self.addSubCategory)
		self.main_layout.addWidget(self.addCategoryWidget)
		

	def create_connections(self):
		pass