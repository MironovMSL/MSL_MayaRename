try:
    from PySide2 import QtWidgets, QtGui, QtCore
    from PySide2.QtWidgets import QAction
except:
    from PySide6 import QtWidgets, QtGui, QtCore
    from PySide6.QtGui import QAction

from MSL_MayaRename.core.resources import Resources


class CacheButtonLibrary(QtWidgets.QPushButton):
	"""
	A custom button class that emits a signal when clicked and provides
	a context menu for additional options like renaming and deletion.
	"""

	itClickedName = QtCore.Signal(str)

	Style_btn = """
	    QPushButton {
	        background-color: rgb(50, 50, 50);
	        
	        border-style: outset;
	        border-width: 2px;
	        border-radius: 8px;
	        border-color: rgb(30, 30, 30);
	        font-family: Roboto; /* Helvetica, Calibri, Verdana, Tahoma, Segoe UI, Open Sans, Source Sans Pro;*/
	        color: rgb(200, 200, 200);
	        padding: 0px;
	    }
	    QPushButton:hover {
	        border-color: rgb(70, 70, 70);
	        background-color: rgb(80, 80, 80);
	    }
	    QPushButton:pressed {
	        background-color: rgb(30, 30, 30);
	        border-style: inset;
	        color: rgb(220, 220, 220);
	    }
	"""



	def __init__(self, name="", width = 40, height = 25, parent=None):
		super(CacheButtonLibrary, self).__init__(parent)
		
		# Attribute---------------------------
		self.name       = name
		self._width     = width
		self._height    = height
		self.toolTip    = f"Button name [{self.name}]"
		# Setting---------------------------
		self.setFixedHeight(self._height)
		self.setText(self.name)
		self.setStyleSheet(self.Style_btn)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.setFont(QtGui.QFont("Verdana", 10))
		self.setToolTip(self.toolTip)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	def __repr__(self):
		return f"Class 'CacheButtonLibrary': [{self.name}]"
	
	def create_widgets(self):
		self.pop_up_window   = PopUpWindow(self.name, self)

	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

	def create_connections(self):

		self.clicked.connect(self.on_clicked)
		self.customContextMenuRequested.connect(self.show_pop_up_window)
		self.pop_up_window.button_delete.clicked.connect(self.on_delete_btn)
	
	def setText(self, name):
		super().setText(name)
		self.adjustSize()
		
	def show_pop_up_window(self, pos):
		"""
		Displays the pop-up window at the position of the button.
		"""
		pop_up_pos = self.mapToGlobal(QtCore.QPoint(self.width() - 35, self._height))

		self.pop_up_window.move(pop_up_pos)
		self.pop_up_window.show()

	def on_clicked(self):
		"""
		Emits the signal when the button is clicked.
		"""
		self.itClickedName.emit(self.text())

	def on_delete_btn(self):
		"""
		Deletes the button from the layout.
		"""
		print(f"Delete button [{self.name}]")
		self.deleteLater()

	def enterEvent(self, event):
		super(CacheButtonLibrary, self).enterEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)

	def leaveEvent(self, event):
		super(CacheButtonLibrary, self).leaveEvent(event)
		self.setStyleSheet(self.Style_btn)
		self.setCursor(QtCore.Qt.ArrowCursor)


class PopUpWindow(QtWidgets.QWidget):
	"""
	Class for creating a pop-up window with options.
	"""

	def __init__(self, name, parent=None):
		super(PopUpWindow, self).__init__(parent)

		# Attribute---------------------------
		self.name = name
		# Setting---------------------------
		self.setWindowTitle(f"{self.name} Options")
		self.setWindowFlags(QtCore.Qt.Popup)
		self.setFixedSize(35, 35)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layout()

	def create_widgets(self):
		self.button_delete = CustomPushButtonLibraryPopUP(self.name, 25, 25)

	def create_layout(self):
		# main layout---------------------------
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_layout.setSpacing(2)
		# add widget---------------------------
		self.main_layout.addWidget(self.button_delete)


	def create_connections(self):
		pass


class CustomPushButtonLibraryPopUP(QtWidgets.QPushButton):
	"""
	Sets a new name for the input field.
	"""

	Style_btn = """
				    QPushButton {
				        background-color: rgb(50, 50, 50); /* Темно-серый фон */
				        border-style: outset;
				        border-width: 2px;
				        border-radius: 8px;
				        border-color: rgb(30, 30, 30); /* Темнее границы */
				        font: normal 12px; /* Жирный шрифт */
				        font-family: Roboto; /* Шрифт Arial */ Helvetica, Calibri, Verdana, Tahoma, Segoe UI, Open Sans, Roboto, Source Sans Pro
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

	def __init__(self, name = "", width = 25, height = 25, parent=None):
		super(CustomPushButtonLibraryPopUP, self).__init__(parent)

		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon    = self.resources.get_icon_from_resources("delete-svgrepo-com.svg")
		self.name    = name
		self._width   = width
		self._height  = height
		self.toolTip = f"Delete button [{self.name}]"
		# Setting---------------------------
		self.setFixedSize(self._width, self._height)
		self.setStyleSheet(self.Style_btn)
		self.setToolTip(self.toolTip)
		self.setIcon(self.icon)

	def set_new_name(self, new_name):
		if new_name != self.name:
			self.name = new_name
			self.toolTip = f"Delete button [{self.name}]"
			self.setToolTip(self.toolTip)

	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(CustomPushButtonLibraryPopUP, self).enterEvent(event)

	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(CustomPushButtonLibraryPopUP, self).leaveEvent(event)