try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources


class FindBytton(QtWidgets.QPushButton):
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

	def __init__(self, parent=None):
		super(FindBytton, self).__init__(parent)
		
		# Module---------------------------
		self.resoures = Resources.get_instance()
		# Attribute---------------------------
		self.icon = self.resoures.get_icon_from_resources("search-find-svgrepo-com.svg")
		tooltip = "Search a name of objef objects"
		# Setting---------------------------
		self.setFixedSize(25, 25)
		self.setToolTip(tooltip)
		self.setStyleSheet(self.Style_btn)
		self.setIcon(self.icon)
		# self.setIconSize(QtCore.QSize(20, 20))
	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(FindBytton, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(FindBytton, self).leaveEvent(event)