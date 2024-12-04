try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.core.common import *
import os


class AddByttonWidget(QtWidgets.QPushButton):
	Style_btn = """
	    QPushButton {
	        background-color: rgb(50, 50, 50); /* Темно-серый фон */
	        border-style: outset;
	        border-width: 2px;
	        border-radius: 8px;
	        border-color: rgb(30, 30, 30); /* Темнее границы */
	        font: bold 14px; /* Жирный шрифт */
	        font-family: Arial; /* Шрифт Arial */
	        color: rgb(200, 200, 200); /* Светло-серый текст */
	        padding: 5px; /* Внутренние отступы */
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

	def __init__(self, name="", width=25, height=25,tooltip="", icon="", parent=None):
		super(AddByttonWidget, self).__init__(name, parent)
		# Attribute---------------------------
		self.width    = width
		self.height   = height
		self.resoures = Resources.get_instance()
		tooltip = f"add the {tooltip} in selected objects"
		# Setting---------------------------
		self.setFixedSize(self.width,self.height)
		self.setToolTip(tooltip)
		self.setStyleSheet(self.Style_btn)

		if icon:
			self.icon     = self.resoures.get_icon_from_resources(icon)
			self.setIcon(self.icon)
	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(AddByttonWidget, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(AddByttonWidget, self).leaveEvent(event)