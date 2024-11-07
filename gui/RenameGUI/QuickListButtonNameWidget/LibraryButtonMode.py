from logging import fatal

from imath import trunc

try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.LibraryGUI import LibraryWindow


class LibraryButtonMode(QtWidgets.QPushButton):

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

	def __init__(self, width=25,height=25, parent=None):
		super(LibraryButtonMode, self).__init__(parent)

		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.width     = width
		self.height    = height
		self.tooltip   = f"Library of names"
		self.icon      = self.resources.get_icon_from_resources("pen-svgrepo-com.svg")
		self.has_state = self.resources.config.get_variable("library", "library_mode", False, bool)
		# Setting---------------------------
		self.setFixedSize(self.width,self.height)
		self.setToolTip(self.tooltip)
		self.setStyleSheet(self.Style_btn)
		self.setIcon(self.icon)
		self.setCheckable(True)
		self.setChecked(self.has_state)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_connections()
		self.show_library(self.has_state)
	
	def create_widgets(self):
		self.Library_Win = LibraryWindow()
	
	def create_connections(self):
		self.clicked.connect(self.is_active_mode)
		self.Library_Win.library_show.connect(self.state_button)

	def is_active_mode(self, state):
		self.show_library(state)
		self.state_button(state)
		
	
	def state_button(self, state):
		if  not self.state_close_window:
			self.resources.config.set_variable("library", "library_mode", state)
			self.has_state = state
			self.setChecked(self.has_state)
			print(f"TODO: library: {'Open UI' if state else 'Close UI'}:")
		self.state_close_window = False
		
	def show_library(self, state):
		if state:
			# mainWindow = self.parent().parent().parent()
			#
			# # posX = mainWindow.geometry().left() + mainWindow.geometry().width()
			# posX = mainWindow.geometry().left()
			# posY = mainWindow.y() + mainWindow.frameGeometry().height()
			self.Library_Win.move(-338, 740) # -338 740
			self.Library_Win.show()
			self.state_close_window = False
			
			# print(posX, posY, )
		else:
			self.state_close_window = True
			self.Library_Win.close()
	
