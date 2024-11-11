try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.addCategoryButtonWidget import addCategoryButtonWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.addSubCategoryButtonWidget import addSubCategoryButtonWidget
import time
import random


class AdditionButtonsWidget(QtWidgets.QWidget):

	Style_btn = """
	        QPushButton {
	            background-color: rgb(70, 70, 70); /* Темно-серый фон */
	            border-style: outset;
	            border-width: 2px;
	            border-radius: 8px;
	            border-color: rgb(30, 30, 30); /* Темнее границы */
	            font: bold 14px; /* Жирный шрифт */
	            font-family: Arial; /* Шрифт Arial */
	            color: rgb(200, 200, 200); /* Светло-серый текст */
	            padding: 0px; /* Внутренние отступы */
	        }

	        QPushButton:hover {
	            border-color: rgb(70, 70, 70); /* Светло-серая граница при наведении */
	            background-color: rgb(80, 80, 80); /* Более светлый серый при наведении */
	        }

	        QPushButton:pressed {
	            background-color: rgb(30, 30, 30); /* Почти черный при нажатии */
	            border-style: inset; /* Впадение при нажатии */
	            color: rgb(220, 220, 220); /* Почти белый текст при нажатии */
	        }

	        QPushButton:checked {
	            background-color: rgb(80, 120, 80); /* Зеленоватый оттенок при нажатии (состояние check) */
	            border-color: rgb(60, 90, 60); /* Темно-зеленая граница при нажатии */
	            color: rgb(240, 240, 240); /* Белый текст */
	        }

	        QPushButton:checked:hover {
	            background-color: rgb(100, 140, 100); /* Светлее при наведении в состоянии checked */
	            border-color: rgb(80, 110, 80); /* Светлее при наведении в состоянии checked */
	        }
	    """
	def __init__(self, parent=None, ):
		super(AdditionButtonsWidget, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		# Setting---------------------------
		self.setFixedHeight(25)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	def create_widgets(self):
		self.addCategory = addCategoryButtonWidget()
		self.addSubCategory = addSubCategoryButtonWidget()

	def create_layouts(self):
		# main layout---------------------------
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)
		# add widget---------------------------
		self.main_layout.addWidget(self.addCategory)
		self.main_layout.addWidget(self.addSubCategory)

	def create_connections(self):
		pass