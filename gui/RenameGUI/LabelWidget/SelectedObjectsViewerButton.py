try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources


class SelectedObjectsViewerButton(QtWidgets.QPushButton):

	Style_btn = """
	        QPushButton {
	            background-color: rgb(50, 50, 50); /* Темно-серый фон */
	            border-style: outset;
	            border-width: 2px;
	            border-radius: 8px;
	            border-color: rgb(30, 30, 30); /* Темнее границы */
	            font: bold 12px; /* Жирный шрифт */
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

	def __init__(self, name="", width=25,height=25, parent=None):
		super(SelectedObjectsViewerButton, self).__init__(parent)

		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.name      = name
		self.width     = width
		self.height    = height
		self.tooltip   = f"Selected objects viewer"
		self.has_state = self.resources.config.get_variable("selected_objects","selected_mode", False, bool)
		# Setting---------------------------
		self.setText(self.name)
		self.setFixedSize(self.width,self.height)
		self.setToolTip(self.tooltip)
		self.setStyleSheet(self.Style_btn)
		self.setCheckable(True)
		self.setChecked(self.has_state)
		# Run functions ---------------------------
		self.create_connections()

	def create_connections(self):
		self.clicked.connect(self.is_active_mode)

	def is_active_mode(self, state):
		self.resources.config.set_variable("selected_objects", "selected_mode", state)
		print(f"TODO: Selected Objects Viewer: {'Open UI' if state else 'Close UI'}:")
	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(SelectedObjectsViewerButton, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(SelectedObjectsViewerButton, self).leaveEvent(event)
