try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.core.common import *
import os


class RenameButtonWidget(QtWidgets.QPushButton):
	
	itCache = QtCore.Signal()
	Style_btn = """
	    QPushButton {
	        background-color: rgb(50, 50, 50); /* Темно-серый фон */
	        border-style: outset;
	        border-width: 2px;
	        border-radius: 8px;
	        border-color: rgb(30, 30, 30); /* Темнее границы */
	        font: normal 12px; /* Жирный шрифт */
	        font-family: Roboto; /* Шрифт Arial  Helvetica, Calibri, Verdana, Tahoma, Segoe UI, Open Sans, Roboto, Source Sans Pro */
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
	"""

	def __init__(self, name="", width=25, height=25, parent=None):
		super(RenameButtonWidget, self).__init__(name, parent)

		# Attribute---------------------------
		self.width    = width
		self.height   = height
		self.tooltip = f"Rename objects"
		# Setting---------------------------
		self.setFixedSize(self.width,self.height)
		self.setToolTip(self.tooltip)
		self.setStyleSheet(self.Style_btn)
		# Run functions ---------------------------
		self.create_connections()

	def create_connections(self):
		pass
