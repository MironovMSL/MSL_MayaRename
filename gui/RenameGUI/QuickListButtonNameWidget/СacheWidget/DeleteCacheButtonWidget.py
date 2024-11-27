try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources


class DeleteCacheButtonWidget(QtWidgets.QPushButton):
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
	
	def __init__(self, width=25, height=25, parent=None):
		super(DeleteCacheButtonWidget, self).__init__(parent)
		
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.width   = width
		self.height  = height
		self.tooltip = f"Delete the button"
		self.icon    = self.resources.get_icon_from_resources("delete-svgrepo-com.svg")
		# Setting---------------------------
		self.setFixedSize(self.width, self.height)
		self.setToolTip(self.tooltip)
		self.setStyleSheet(self.Style_btn)
		self.setIcon(self.icon)
		# Run functions ---------------------------
		self.create_connections()
	
	def create_connections(self):
		pass

	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(DeleteCacheButtonWidget, self).enterEvent(event)

	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(DeleteCacheButtonWidget, self).leaveEvent(event)
