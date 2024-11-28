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
	itShowCache = QtCore.Signal(bool)
	
	def __init__(self, width=25, height=25, parent=None):
		super(LibraryButtonMode, self).__init__(parent)

		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self._width     = width
		self._height    = height
		self.tooltip   = f"Library of names"
		self.icon      = self.resources.get_icon_from_resources("pen-svgrepo-com.svg")
		self.has_state = self.resources.config.get_variable("library", "library_mode", False, bool)
		# Setting---------------------------
		self.setFixedSize(self._width,self._height)
		self.setToolTip(self.tooltip)
		self.setStyleSheet(self.Style_btn)
		self.setIcon(self.icon)
		self.setCheckable(True)
		self.setChecked(self.has_state)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_connections()
		self.show_library(self.has_state)
	
	def create_widgets(self):
		self.Library_Win = LibraryWindow()
		self.pop_up_window = PopUpWindow("library", self)
	
	def create_connections(self):
		self.clicked.connect(self.is_active_mode)
		self.Library_Win.library_show.connect(self.state_button)
		self.Library_Win.itSave.connect(self.update_words_complete)
		self.customContextMenuRequested.connect(self.show_pop_up_window)
		self.pop_up_window.cache_btn.itShowCache.connect(lambda state: self.itShowCache.emit(state))

	def show_pop_up_window(self, pos):
		"""
		Displays the pop-up window at the position of the button.
		"""
		pop_up_pos = self.mapToGlobal(QtCore.QPoint(self._width, 0))

		self.pop_up_window.move(pop_up_pos)
		self.pop_up_window.show()

	def update_words_complete(self):
		"""
		Updates the word list for the autocompletion in RenameWidget(QlineEdit)
		"""
		update_words  = self.resources.get_all_itemJSON()
		self.parent().parent().RenameWidget.LineEditor.word_list = update_words
		self.parent().parent().RenameWidget.LineEditor.update_words()

	def is_active_mode(self, state):
		self.show_library(state)
		self.state_button(state)
	
	def state_button(self, state):
		if  not self.state_close_window:
			self.resources.config.set_variable("library", "library_mode", state)
			self.has_state = state
			self.setChecked(self.has_state)
		self.state_close_window = False
		
	def show_library(self, state):
		self.window_geometry =  self.resources.config.get_variable("startup", "window_geometry", QtCore.QRect(), QtCore.QRect)
		
		try:
			mainWindow = self.parent().parent().parent()
		except:
			mainWindow = None
		
		if state:
			if mainWindow:
				# posX = mainWindow.geometry().left() + mainWindow.geometry().width()
				posX = mainWindow.geometry().left()
				posY = mainWindow.y() + mainWindow.frameGeometry().height()
				self.Library_Win.move(posX, posY)
			else:
				if self.window_geometry:
					pos_x = self.window_geometry.x()
					pos_y = self.window_geometry.y() + 250
					self.Library_Win.move(pos_x, pos_y)
			
			self.Library_Win.show()
			self.state_close_window = False

		else:
			self.state_close_window = True
			self.Library_Win.close()
			
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(LibraryButtonMode, self).enterEvent(event)

	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(LibraryButtonMode, self).leaveEvent(event)
	
class PopUpWindow(QtWidgets.QWidget):
	"""
	Class for creating a pop-up window with options.
	"""

	def __init__(self, name, parent=None):
		super(PopUpWindow, self).__init__(parent)

		# Attribute---------------------------
		self.name = name
		# Setting---------------------------
		self.setWindowTitle(f"Library options")
		self.setWindowFlags(QtCore.Qt.Popup)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layout()

	def create_widgets(self):
		self.cache_btn = CustomPushButtonCachePopUP()

	def create_layout(self):
		layout = QtWidgets.QFormLayout(self)
		layout.addRow("Cache: ", self.cache_btn)
		layout.setContentsMargins(2, 2, 2, 2)
		layout.setSpacing(0)

	def create_connections(self):
		pass


class CustomPushButtonCachePopUP(QtWidgets.QPushButton):
	"""
	Display show the cache.
	"""
	
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
	itShowCache = QtCore.Signal(bool)

	def __init__(self, parent=None):
		super(CustomPushButtonCachePopUP, self).__init__(parent)

		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon      = self.resources.get_icon_from_resources("cache-svgrepo-com.svg")
		self.has_state = self.resources.config.get_variable("library", "show_cache", False, bool)
		self.toolTip   = f"Show the cache"
		# Setting---------------------------
		self.setFixedSize(25, 25)
		self.setStyleSheet(self.Style_btn)
		self.setToolTip(self.toolTip)
		self.setIcon(self.icon)
		self.setCheckable(True)
		self.setChecked(self.has_state)
		
		self.create_connections()
		
		
	def create_connections(self):
		self.clicked.connect(self.on_show_cache)
		
	def on_show_cache(self, state):
		self.resources.config.set_variable("library", "show_cache", state)
		self.has_state = state
		self.setChecked(self.has_state)
		
		self.itShowCache.emit(state)

	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(CustomPushButtonCachePopUP, self).enterEvent(event)

	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(CustomPushButtonCachePopUP, self).leaveEvent(event)