try:
	from PySide2 import QtWidgets, QtGui, QtCore
	from PySide2.QtWidgets import QAction
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	from PySide6.QtGui import QAction

from MSL_MayaRename.core.resources import Resources


class ButtonCategoryWidget(QtWidgets.QPushButton):
	"""
	A custom button class that emits a signal when clicked and provides
	a context menu for additional options like renaming and deletion.
	"""
	
	itClickedName        = QtCore.Signal(str)
	itClickedName_alt        = QtCore.Signal(str)
	drag_button_category = QtCore.Signal()
	itDeleteCategory     = QtCore.Signal()
	
	Style_btn_category = """
	    QPushButton {
	        background-color: rgb(85, 75, 65); /* Теплый оттенок для фона */
	        border-style: outset;
	        border-width: 2px;
	        border-radius: 8px;
	        border-color: rgb(45, 45, 40); /* Темная граница для акцента */
	        font-family: Roboto;
	        color: rgb(235, 235, 225); /* Светлый текст для контраста */
	        padding: 0px;
	    }
	    QPushButton:hover {
	        border-color: rgb(100, 90, 80); /* Яркая граница при наведении */
	        background-color: rgb(105, 95, 85); /* Немного светлее при наведении */
	    }
	    QPushButton:pressed {
	        background-color: rgb(65, 55, 45); /* Глубокий цвет при нажатии */
	        border-style: inset;
	        color: rgb(245, 245, 235); /* Самый светлый текст при нажатии */
	    }
	"""
	
	def __init__(self, name="", width=40, height=25, parent=None):
		super(ButtonCategoryWidget, self).__init__(parent)

		# Attribute---------------------------
		self.name    = name
		self._width  = width
		self._height = height
		self.toolTip = f"Button name [{self.name}]"
		# Setting-----------------------------
		self.setFixedSize(self._width, self._height)
		self.setText(self.name)
		self.setStyleSheet(self.Style_btn_category)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.setFont(QtGui.QFont("Verdana", 10))
		self.setToolTip(self.toolTip)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
		self.adjust_font_size()
	
	def __repr__(self):
		return f"Class: ButtonCategoryWidget - [{self.name}]"
	
	def create_widgets(self):
		self.pop_up_window = PopUpWindow(self.name, self)
	
	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
	
	def create_connections(self):
		self.customContextMenuRequested.connect(self.show_pop_up_window)
		self.pop_up_window.button_delete.clicked.connect(lambda: self.itDeleteCategory.emit())
		self.pop_up_window.rename_linEdit.textEdited.connect(self.on_change_text)
		self.pop_up_window.rename_linEdit.returnPressed.connect(self.pop_up_window.close)
	
	def on_change_text(self, text):
		"""
		Updates the button name and tooltip when the text in the
		pop-up window's line edit changes.
		"""
		old_name = self.name
		self.set_new_name(text)
		self.pop_up_window.button_delete.set_new_name(text)
		self.pop_up_window.rename_linEdit.set_new_name(text)
		self.adjust_font_size()
	
	def set_new_name(self, new_name):
		if new_name != self.name:
			self.name = new_name
			self.setText(self.name)
			self.toolTip = f"Button name [{self.name}]"
			self.setToolTip(self.toolTip)
	
	def adjust_font_size(self):
		"""
		Adjusts the font size of the button text to fit within its dimensions.
		"""
		font = self.font()
		font_size = 10  # Initial font size
		button_width = self.width() - 2  # Consider a small indent
		
		while font_size > 1:
			font.setPointSize(font_size)
			metrics = QtGui.QFontMetrics(font)
			text_width = metrics.horizontalAdvance(self.text())
			if text_width <= button_width:
				break
			font_size -= 1
		
		self.setFont(font)
		self.update()  # Forced interface update
	
	def show_pop_up_window(self, pos):
		"""
		Displays the pop-up window at the position of the button.
		"""
		pop_up_pos = self.mapToGlobal(QtCore.QPoint(0, self._height))
		
		self.pop_up_window.move(pop_up_pos)
		self.pop_up_window.rename_linEdit.setFocus()
		self.pop_up_window.rename_linEdit.selectAll()
		
		self.pop_up_window.show()
	
	def enterEvent(self, event):
		super(ButtonCategoryWidget, self).enterEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)
	
	def leaveEvent(self, event):
		super(ButtonCategoryWidget, self).leaveEvent(event)
		self.setStyleSheet(self.Style_btn_category)
		self.setCursor(QtCore.Qt.ArrowCursor)
	
	def mouseReleaseEvent(self, event):
		super(ButtonCategoryWidget, self).mouseReleaseEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)
	
	def mousePressEvent(self, event):
		super(ButtonCategoryWidget, self).mousePressEvent(event)
		
		if event.button() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.AltModifier:
			self.itClickedName_alt.emit(self.text())
		elif event.button() == QtCore.Qt.LeftButton:
			self.itClickedName.emit(self.text())
		
		if hasattr(QtCore.Qt, "MiddleButton"):
			middle_button = QtCore.Qt.MiddleButton  # Для Qt6
		else:
			middle_button = QtCore.Qt.MidButton  # Для Qt5
		
		if event.button() != middle_button:
			return
		
		self.setCursor(QtCore.Qt.ClosedHandCursor)
		self.drag_button_category.emit()
		
		# Create MIME data and set text
		mimeData = QtCore.QMimeData()
		mimeData.setText(self.text())
		
		# Capture the button image
		self.pixmap = self.parent().grab()
		radius = 8  # Set the rounding radius
		rounded_mask = QtGui.QBitmap(self.pixmap.size())  # Create a circular mask taking into account the radius
		rounded_mask.fill(QtCore.Qt.color0)  # Fully transparent background for the mask
		painter = QtGui.QPainter(rounded_mask)
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		painter.setBrush(QtCore.Qt.color1)  # Color that will be visible
		painter.drawRoundedRect(self.pixmap.rect(), radius, radius)  # Rounded rectangle to fit button size
		painter.end()
		# Set a mask on the image
		self.pixmap.setMask(rounded_mask)
		# Darken the image to create a "ghost"
		painter = QtGui.QPainter(self.pixmap)
		painter.setCompositionMode(QtGui.QPainter.CompositionMode_DestinationIn)
		painter.fillRect(self.pixmap.rect(), QtGui.QColor(80, 80, 80, 200))  # Only transparency is applied, RGB color is not applied
		painter.end()
		
		# Create a QDrag object and configure it
		drag = QtGui.QDrag(self)
		drag.setMimeData(mimeData)
		drag.setPixmap(self.pixmap)
		drag.setHotSpot(event.pos())  # Set the capture point
		
		drag.exec_(QtCore.Qt.LinkAction | QtCore.Qt.MoveAction)  # Start the drag and drop action

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
		self.setFixedSize(117, 35)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layout()
	
	def create_widgets(self):
		self.rename_linEdit = CustomQLineEditLibraryPopUP(self.name, 80, 25)
		self.button_delete  = CustomPushButtonLibraryPopUP(self.name, 25, 25)
	
	def create_layout(self):
		# main layout---------------------------
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_layout.setSpacing(2)
		# add widget---------------------------
		self.main_layout.addWidget(self.rename_linEdit)
		self.main_layout.addWidget(self.button_delete)
		self.main_layout.addStretch()
	
	def create_connections(self):
		pass

class CustomQLineEditLibraryPopUP(QtWidgets.QLineEdit):
	"""
	Class for creating a customizable input field.
	"""
	
	Style_lineEdit = """
		    QLineEdit {
		        background-color: rgb(40, 40, 40);  /* Темно-серый фон */
		        border: 2px solid rgb(100, 100, 100);  /* Серо-черная граница */
		        border-radius: 10px;
		        padding: 0 4px;
		        color: rgb(220, 220, 220);          /* Светло-серый текст */
		        selection-background-color: rgb(88, 88, 120); /* Темно-серый фон для выделения */
		        selection-color: rgb(255, 255, 255);  /* Белый текст при выделении */
		    }

		    QLineEdit:hover {
		        border: 2px solid rgb(100, 100, 100);  /* Светло-серая граница при наведении */
		        background-color: rgb(45, 45, 45);     /* Немного светлее при наведении */
		    }

		    QLineEdit:focus {
		        color: rgb(255, 255, 255);           /* Белый текст при фокусе */
		        border: 2px solid rgb(120, 120, 120); /* Ярче серый при фокусе */
		        background-color: rgb(50, 50, 50);    /* Более светлый серый при фокусе */
		    }

		    QLineEdit:hover:focus {
		        border: 2px solid rgb(150, 150, 150); /* Светлая граница при наведении и фокусе */
		        background-color: rgb(55, 55, 55);    /* Еще более светлый фон при наведении и фокусе */
		    }
		"""
	
	def __init__(self, name="", width=40, height=25, parent=None):
		super(CustomQLineEditLibraryPopUP, self).__init__(parent)
		# Attribute---------------------------
		self._width = width
		self._height = height
		self.name = name
		self.toolTip = f"Change name button [{self.name}]"
		# Setting---------------------------
		self.setText(self.name)
		self.setFixedSize(self._width, self._height)
		self.setStyleSheet(self.Style_lineEdit)
		self.setToolTip(self.toolTip)
		self.setAlignment(QtCore.Qt.AlignHCenter)
	
	def set_new_name(self, new_name):
		if new_name != self.name:
			self.name = new_name
			self.toolTip = f"Change name button [{self.name}]"
			self.setToolTip(self.toolTip)
	
	def contextMenuEvent(self, event):
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
	
	def __init__(self, name="", width=25, height=25, parent=None):
		super(CustomPushButtonLibraryPopUP, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon      = self.resources.get_icon_from_resources("delete-svgrepo-com.svg")
		self.name      = name
		self._width    = width
		self._height   = height
		self.toolTip   = f"Delete button [{self.name}]"
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