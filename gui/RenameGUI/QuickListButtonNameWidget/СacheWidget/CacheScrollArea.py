try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.СacheWidget.CacheButtonLibrary import CacheButtonLibrary
import time


class CacheScrollArea(QtWidgets.QScrollArea):
	"""
	A custom scroll area that contains a scrollable content widget with buttons.
	It allows horizontal scrolling using the mouse wheel.
	"""
	itClickedName = QtCore.Signal(str)

	def __init__(self, key=None, parent=None, ):
		super(CacheScrollArea, self).__init__(parent)
		# Modul---------------------------
		self.resources    = Resources.get_instance()
		# Attribute---------------------------
		self.button_width = 60
		self.ScrollBar    = CustemQScrollBar(self)
		# Setting---------------------------
		self.setObjectName("CacheScrollArea")
		# self.setFixedWidth(280)
		self.setWidgetResizable(True)
		self.setFocusPolicy(QtCore.Qt.NoFocus)
		self.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setHorizontalScrollBar(self.ScrollBar)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()

	def create_widgets(self):
		self.scroll_area_widget = ScrolContentWidget(self.button_width, self)

	def create_layouts(self):
		self.setWidget(self.scroll_area_widget)

	def create_connections(self):
		self.scroll_area_widget.itClickedName.connect(self.emit_signal)
		
	def emit_signal(self, text):
		print(f"emit_signal from CustomScrollArea: {text}")
		self.itClickedName.emit(text)
	
	def wheelEvent(self, event):
		"""Overriding the wheel event for horizontal scrolling"""
		delta = event.angleDelta().y()  # Get the mouse wheel change


		if delta > 0:
			new_value = self.horizontalScrollBar().value() - 40
		else:
			new_value = self.horizontalScrollBar().value() + 40
		
		# Limit the value within the acceptable range
		new_value = max(0, min(new_value, self.horizontalScrollBar().maximum()))
		self.horizontalScrollBar().setValue(new_value)


class ScrolContentWidget(QtWidgets.QWidget):
	"""
	A custom QWidget that contains scrollable buttons based on a provided list of words.
	The widget supports drag-and-drop functionality for reordering buttons.
	"""
	
	itClickedName = QtCore.Signal(str)

	def __init__(self, width = 60, parent=None):
		super(ScrolContentWidget, self).__init__(parent)
		
		# Modul---------------------------
		# Attribute---------------------------
		self._height           = 25
		self._width            = width
		# Setting---------------------------
		self.setFixedHeight(self._height)
		# Run functions ---------------------------
		self.create_widgets()
		self.creat_layout()
		self.create_connections()

	def create_widgets(self):
		pass

	def creat_layout(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
	
	def create_connections(self):
		pass
	

	def add_button(self, text):
		"""
		Adds a button with the given text to the layout if it doesn't already exist.
		"""
		for i in range(self.main_layout.count()):
			existing_button = self.main_layout.itemAt(i).widget()
			if isinstance(existing_button, CacheButtonLibrary) and existing_button.text() == text:
				print(f"Button with name '{text}' already exists, adding cancelled.")
				return
		
		# If the button is not found, create and add a new one
		button = CacheButtonLibrary(text, self._width, self._height)
		self.main_layout.addWidget(button)
		button.itClickedName.connect(self.emit_signal)

		return button
	
	def emit_signal(self, text):
		self.itClickedName.emit(text)
		
			
class CustemQScrollBar(QtWidgets.QScrollBar):
	"""
	A custom horizontal scrollbar with a specific style and behavior for horizontal scrolling.
	"""
	scroll_style = """
	    QScrollBar:horizontal {
	        background: rgb(10, 10, 10); /* Very dark gray background */
	        height: 5px;
	        margin: 0px 0px 0px 0px;
	    }
	    QScrollBar::handle:horizontal {
	        background: rgb(50, 50, 50); /* Dark gray matching button background */
	        border: 1px solid rgb(30, 30, 30); /* Dark border to match button */
	        min-width: 20px;
	        border-radius: 3px;
	    }
	    QScrollBar::handle:horizontal:hover {
	        background: rgb(80, 80, 80); /* Slightly lighter gray on hover */
	        border: 1px solid rgb(70, 70, 70); /* Light gray border on hover */
	    }
	    QScrollBar::handle:horizontal:pressed {
	        background: rgb(30, 30, 30); /* Almost black when pressed */
	        border: 1px solid rgb(20, 20, 20); /* Dark border when pressed */
	    }
	    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
	        width: 0px;
	        height: 0px;
	    }
	"""
	
	def __init__(self, parent = None):
		super(CustemQScrollBar, self).__init__(parent)
		
		self.setStyleSheet(self.scroll_style)
		self.step_size = 40
	
	def wheelEvent(self, event):
		"""Overriding the wheel event for horizontal scrolling"""
		delta = event.angleDelta().y()  # Get the mouse wheel change
		if self.orientation() == QtCore.Qt.Horizontal:
			if delta > 0:
				self.setValue(self.value() - self.step_size)  # Scroll left
			else:
				self.setValue(self.value() + self.step_size)  # Scroll right
		else:
			if delta > 0:
				self.setValue(self.value() - self.step_size)  # Scroll up
			else:
				self.setValue(self.value() + self.step_size)
		
		# Limit the value within the acceptable range
		self.setValue(max(self.minimum(), min(self.value(), self.maximum())))
		
	def enterEvent(self, event):
		super(CustemQScrollBar, self).enterEvent(event)
		self.setCursor(QtCore.Qt.OpenHandCursor)
	
	def leaveEvent(self, event):
		super(CustemQScrollBar, self).leaveEvent(event)
		self.setCursor(QtCore.Qt.ArrowCursor)
	
	def mouseReleaseEvent(self, event):
		super(CustemQScrollBar, self).mouseReleaseEvent(event)
		self.setCursor(QtCore.Qt.OpenHandCursor)
	
	def mousePressEvent(self, event):
		super(CustemQScrollBar, self).mousePressEvent(event)
		self.setCursor(QtCore.Qt.ClosedHandCursor)
		
		