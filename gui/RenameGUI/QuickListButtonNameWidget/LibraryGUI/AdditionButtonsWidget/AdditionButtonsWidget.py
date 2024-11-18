from maya.cmds import srtContext

try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.addCategoryButtonWidget import addCategoryButtonWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.addCategoryWidget import addCategoryWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.addSubCategoryButtonWidget import addSubCategoryButtonWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.addSubCategoryWidget import addSubCategoryWidget

class AdditionButtonsWidget(QtWidgets.QWidget):
	isCategoryName = QtCore.Signal(str)
	isSubCategoryName = QtCore.Signal(str, str)

	def __init__(self, parent=None, ):
		super(AdditionButtonsWidget, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.category = self.resources.config.get_variable("library", "category_mode", False, bool)
		self.subCategory = self.resources.config.get_variable("library", "sub_category_mode", False, bool)
		# Setting---------------------------
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.setFixedHeight(25)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	def create_widgets(self):
		self.addCategory_BTN      = addCategoryButtonWidget(self.category)
		self.addSubCategory_BTN   = addSubCategoryButtonWidget(self.subCategory)
		self.addCategoryWidget    = addCategoryWidget(self.category)
		self.addSubCategoryWidget = addSubCategoryWidget(self.subCategory)

	def create_layouts(self):
		# main layout---------------------------
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
		# add widget---------------------------
		self.main_layout.addWidget(self.addCategory_BTN)
		self.main_layout.addWidget(self.addSubCategory_BTN)
		self.main_layout.addWidget(self.addCategoryWidget)
		self.main_layout.addWidget(self.addSubCategoryWidget)

	def create_connections(self):
		self.addCategory_BTN.isChangeState.connect(self.update_state)
		self.addSubCategory_BTN.isChangeState.connect(self.update_state)
		self.addCategoryWidget.isCategoryName.connect(lambda name: self.isCategoryName.emit(name))
		self.addSubCategoryWidget.isSubCategoryName.connect(lambda name, category: self.isSubCategoryName.emit(name, category))
	
	def _animate_widget(self, widget, start_rect, end_rect, duration=500):
		animation = QtCore.QPropertyAnimation(widget, b"geometry")
		animation.setDuration(duration)
		animation.setStartValue(start_rect)
		animation.setEndValue(end_rect)
		animation.setEasingCurve(QtCore.QEasingCurve.OutCubic)
		animation.start()
		return animation
	
	def update_state(self, state):
		who = self.sender()
		
		if who == self.addCategory_BTN:
			if state:
				self.addCategoryWidget.setVisible(True)
				end_width = self.size().width() - 50
				start_rect = QtCore.QRect(50, 0, 50, 25)
				end_rect = QtCore.QRect(50, 0, end_width, 25)
				self.animate_add_category = self._animate_widget(self.addCategoryWidget, start_rect, end_rect)
			else:
				start_rect = self.addCategoryWidget.geometry()
				end_rect = self.addCategoryWidget.geometry()
				end_rect.setWidth(0)
				self.animate_add_category = self._animate_widget(self.addCategoryWidget, start_rect, end_rect)
				self.animate_add_category.finished.connect(lambda: self.addCategoryWidget.setVisible(False))
			
			if self.addSubCategory_BTN.isChecked():
				self.addSubCategory_BTN.setChecked(False)
				self.addSubCategory_BTN.set_state(False)

				end_width = self.size().width()
				start_rect = self.addSubCategoryWidget.geometry()
				end_rect = QtCore.QRect(end_width, 0, end_width, 25)
				
				self.animate_add_subcategory = self._animate_widget(self.addSubCategoryWidget, start_rect, end_rect)
				self.animate_add_subcategory.finished.connect(lambda: self.addSubCategoryWidget.setVisible(False))
		
		elif who == self.addSubCategory_BTN:
			if state:
				self.addSubCategoryWidget.setVisible(True)
				end_width = self.size().width() - 50
				start_rect = QtCore.QRect(50, 0, 50, 25)
				end_rect = QtCore.QRect(50, 0, end_width, 25)
				self.animate_add_subcategory = self._animate_widget(self.addSubCategoryWidget, start_rect, end_rect)
			else:
				start_rect = self.addSubCategoryWidget.geometry()
				end_rect = self.addSubCategoryWidget.geometry()
				end_rect.setWidth(0)
				self.animate_add_subcategory = self._animate_widget(self.addSubCategoryWidget, start_rect, end_rect)
				self.animate_add_subcategory.finished.connect(lambda: self.addSubCategoryWidget.setVisible(False))
			
			if self.addCategory_BTN.isChecked():
				self.addCategory_BTN.setChecked(False)
				self.addCategory_BTN.set_state(False)

				end_width = self.size().width()
				start_rect = self.addCategoryWidget.geometry()
				end_rect = QtCore.QRect(end_width, 0, end_width, 25)
				self.animate_add_category = self._animate_widget(self.addCategoryWidget, start_rect, end_rect)
				self.animate_add_category.finished.connect(lambda: self.addCategoryWidget.setVisible(False))
				