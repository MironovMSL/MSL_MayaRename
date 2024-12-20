try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.LibraryScrollAreaWidget.ButtonCategoryWidget import ButtonCategoryWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.LibraryScrollAreaWidget.ScrollAreaCategoryWidget import ScrollAreaCategoryWidget
import time

class CategoryWidget(QtWidgets.QWidget):
	
	itClickedName = QtCore.Signal(str)
	itClickedName_alt = QtCore.Signal(str)
	drag_button_category = QtCore.Signal(object)
	itDeleteCategory = QtCore.Signal(object, str)
	
	def __init__(self, name, width = 60, height = 25, main_key=None, parent = None):
		super(CategoryWidget, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.main_key = main_key if main_key is not None else "ListName"
		self.name    = name
		self._width  = width
		self._height = height
		# Setting---------------------------
		self.setFixedWidth(self._width)
		self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	def __repr__(self):
		return f"Class: CategoryWidget - [{self.name}]"
	
	def create_widgets(self):
		self.category_button = ButtonCategoryWidget(self.name,self._width, self._height)
		self.category_widget = ScrollAreaCategoryWidget(self.name, self._width, 20, self.main_key)
		
	def create_layouts(self):
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		
		self.main_layout.addWidget(self.category_button)
		self.main_layout.addWidget(self.category_widget)
	
	def create_connections(self):
		self.category_button.itClickedName.connect(lambda name: self.itClickedName.emit(name))
		self.category_button.itClickedName_alt.connect(lambda name: self.itClickedName_alt.emit(name))
		self.category_widget.itClickedName.connect(lambda name: self.itClickedName.emit(name))
		self.category_widget.itClickedName_alt.connect(lambda name: self.itClickedName_alt.emit(name))
		self.category_button.drag_button_category.connect(lambda: self.drag_button_category.emit(self))
		self.category_button.itDeleteCategory.connect(lambda: self.itDeleteCategory.emit(self, self.name))