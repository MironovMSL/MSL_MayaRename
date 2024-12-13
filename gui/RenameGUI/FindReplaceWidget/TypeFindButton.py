try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources


class TypeFindButton(QtWidgets.QPushButton):
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
	TYPE_LIST = ["selected", "hierarchy", "all"]
	
	
	def __init__(self, parent=None):
		super(TypeFindButton, self).__init__(parent)
		# Module---------------------------
		self.resoures = Resources.get_instance()
		# Attribute---------------------------
		self.type = self.resoures.config.get_variable("startup", "type_find", "selected", str)
		tooltip = f"{self.type}"
		# Setting---------------------------
		self.setFixedSize(25, 25)
		self.setToolTip(tooltip)
		self.setStyleSheet(self.Style_btn)
	
		# Run functions ---------------------------
		self.set_name_btn(self.type)

	
	def set_name_btn(self, type):
		if type == "selected":
			name = "sel"
		elif type == "hierarchy":
			name = "hi"
		elif type == "all":
			name = "all"
			
		self.setText(name)
	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(TypeFindButton, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(TypeFindButton, self).leaveEvent(event)
