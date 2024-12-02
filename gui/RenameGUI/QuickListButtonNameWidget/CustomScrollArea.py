try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.CustomButtonLibrary import CustomButtonLibrary
import time


class CustomScrollArea(QtWidgets.QScrollArea):
	"""
	A custom scroll area that contains a scrollable content widget with buttons.
	It allows horizontal scrolling using the mouse wheel.
	"""
	itClickedName = QtCore.Signal(str)
	itClickedName_alt = QtCore.Signal(str)

	def __init__(self, key=None, parent=None, ):
		super(CustomScrollArea, self).__init__(parent)
		# Modul---------------------------
		self.resources    = Resources.get_instance()
		# Attribute---------------------------
		self.word_list    = self.resources.get_itemJSON_from_key(dictionary_name="fast_access")
		self.key          = key
		self.button_width = 40
		self.ScrollBar    = CustemQScrollBar(self.button_width, self)
		# Setting---------------------------
		self.setObjectName("CustomScrollAreaID")
		self.setFixedWidth(280)
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
		self.scroll_area_widget = ScrolContentWidget(self.button_width, 25, self.word_list, self)

	def create_layouts(self):
		self.setWidget(self.scroll_area_widget)

	def create_connections(self):
		self.scroll_area_widget.itClickedName.connect(lambda name:  self.itClickedName.emit(name))
		self.scroll_area_widget.itClickedName_alt.connect(lambda name:  self.itClickedName_alt.emit(name))
		
	def wheelEvent(self, event):
		"""Overriding the wheel event for horizontal scrolling"""
		delta = event.angleDelta().y()  # Get the mouse wheel change
		step_size = self.button_width  # Step width equal to button width

		if delta > 0:
			new_value = self.horizontalScrollBar().value() - step_size
		else:
			new_value = self.horizontalScrollBar().value() + step_size
		
		# Limit the value within the acceptable range
		new_value = max(0, min(new_value, self.horizontalScrollBar().maximum()))
		self.horizontalScrollBar().setValue(new_value)


class ScrolContentWidget(QtWidgets.QWidget):
	"""
	A custom QWidget that contains scrollable buttons based on a provided list of words.
	The widget supports drag-and-drop functionality for reordering buttons.
	"""
	
	itClickedName = QtCore.Signal(str)
	itClickedName_alt = QtCore.Signal(str)
	placeholder_Style = """
		    background-color: rgb(40, 40, 40);
		    border: 4px groove rgb(70, 70, 70);
		    border-radius: 12px;
		    color: rgb(180, 180, 180);
		"""

	def __init__(self, width = 40, height = 25, word_list = [], parent=None):
		super(ScrolContentWidget, self).__init__(parent)
		
		# Modul---------------------------
		# Attribute---------------------------
		self._height           = height
		self._width            = width
		self.word_list         = word_list
		# Attribute scroll---------------------------
		self.scroll_direction  = 0        # Variable for scroll direction
		self.start_time        = None     # Countdown start time
		self.scroll_area       = None     # Assume that MyWidget is nested in QScrollArea
		self.scroll_width      = None     # Scroll area width
		self.info              = None
		self.dragged_button    = None     # Variable to store the draggable button
		self.placeholder_index = None     # Index for pos widget
		# Setting---------------------------
		self.setFixedHeight(self._height)
		self.setAcceptDrops(True)
		# Run functions ---------------------------
		self.create_widgets()
		self.creat_layout()
		self.create_connections()
		self.add_content()
		
	def create_widgets(self):
		self.scroll_timer = QtCore.QTimer(self)
		self.outside_tracking_timer  = QtCore.QTimer(self)

		self.placeholder = QtWidgets.QFrame(self)
		self.placeholder.setFixedSize(self._width, self._height)
		self.placeholder.setStyleSheet(self.placeholder_Style)
		self.placeholder.hide()

	def creat_layout(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
	
	def create_connections(self):
		self.scroll_timer.timeout.connect(self.scroll_content)

	def get_info(self):
		state = False
		if state:
			print(self.info)
			print(self.dragged_button)
			print(self.placeholder_index)
	
	def add_content(self):
		"""
		Adds buttons to the widget based on the word_list attribute.
		Ensures that no duplicate buttons are added.
		"""

		for word in self.word_list:
			self.add_button(word)

	def add_button(self, text):
		"""
		Adds a button with the given text to the layout if it doesn't already exist.
		"""
		for i in range(self.main_layout.count()):
			existing_button = self.main_layout.itemAt(i).widget()
			if isinstance(existing_button, CustomButtonLibrary) and existing_button.text() == text:
				print(f"Button with name '{text}' already exists, adding cancelled.")
				return
		
		# If the button is not found, create and add a new one
		button = CustomButtonLibrary(text, self._width, self._height)
		self.main_layout.addWidget(button)
		button.itClickedName.connect(lambda name: self.itClickedName.emit(name))
		button.itClickedName_alt.connect(lambda name: self.itClickedName_alt.emit(name))
		button.drag_button_name.connect(self.set_dragged_button)
		
		return button
	
	def set_dragged_button(self, button):
		"""
		Sets the currently dragged button to the specified button.
		"""
		self.dragged_button = button

		
	def scroll_content(self):
		"""
		Handles the scrolling logic for the widget based on the current scroll direction.
		"""
		
		if self.scroll_direction != 0:

			pos_scroll_bar = self.scroll_area.horizontalScrollBar().value()
			max_scroll     = self.scroll_area.horizontalScrollBar().maximum()
			
			self.scroll_area.horizontalScrollBar().setValue(pos_scroll_bar + self.scroll_direction * 40)

			if ((pos_scroll_bar == 0 and self.scroll_direction == -1) or
				(pos_scroll_bar == max_scroll and self.scroll_direction == 1)):
				
				self.scroll_direction = 0
				self.scroll_timer.stop()
				self.start_time = None
				
				part = "Stop the timer"
				
			elif self.start_time is not None:
				elapsed_time = time.time() - self.start_time  # Calculate the elapsed time
				part = f"{elapsed_time:.2f} seconds"
				
			self.info = f"[0]=[{pos_scroll_bar}]=[{max_scroll}]: Time: {part}"
			self.get_info()
	
	def enterEvent(self, event):
		self.scroll_timer.stop()
		super().enterEvent(event)
	
	def leaveEvent(self, event):
		self.scroll_timer.stop()
		super().leaveEvent(event)
	
	def dragLeaveEvent(self, event):
		print("dragLeaveEvent")
		
		if self.dragged_button:
			self.main_layout.insertWidget(self.placeholder_index, self.dragged_button)
			self.dragged_button.setVisible(True)
		self.placeholder.hide()
		

	def dragEnterEvent(self, event):
		self.info = "dragEnterEvent"
		if event.mimeData().hasText():
			self.scroll_area  = self.parent().parent()
			self.scroll_width = self.scroll_area.width()
			
			self.get_info()
			event.acceptProposedAction()

	def dragMoveEvent(self, event):
		"""
		Event handler for when a dragged item is moved within the widget. Updates the placeholder position.
		"""
		pos_in_widget       = event.pos()
		pos_in_scroll_area  = self.mapToParent(pos_in_widget).x()
		widget_under_cursor = self.childAt(pos_in_widget)
		
		if widget_under_cursor is None:
			self.placeholder_index = self.main_layout.count() - 1
		else:
			self.placeholder_index = self.main_layout.indexOf(self.childAt(pos_in_widget))

		self.main_layout.insertWidget(self.placeholder_index, self.placeholder)

		if self.dragged_button:
			self.dragged_button.setVisible(False)
		self.placeholder.show()

		if event.mimeData().hasText():
			part = "None"
			if self.width() > self.scroll_width:

				if pos_in_scroll_area < 25:
					part = "Left edge"
					self.scroll_direction = -1
					self.start_scroll_timer()
				elif pos_in_scroll_area > self.scroll_width - 25:
					part = "Right Edge"
					self.scroll_direction = 1
					self.start_scroll_timer()
				else:
					part =  "Stop the timer"
					self.scroll_direction = 0
					self.scroll_timer.stop()
					self.start_time = None

			self.info = (f"Widget pos   - [{pos_in_widget.x()}]:[{pos_in_scroll_area}] - Scroll pos,\n"
			             f"Scroll width - [{self.scroll_width}]:[{self.width()}] - Widget width,\n"
			             f"mimeData     - [{event.mimeData().text()}], Timer - {part}, {self.placeholder_index}: {self.main_layout.count()}")

			self.get_info()

		event.acceptProposedAction()
		
	def start_scroll_timer(self):
		"""
		Starts the scrolling timer if it is not already active.
		"""
		if not self.scroll_timer.isActive():
			self.start_time = time.time()
			self.scroll_timer.start(200)
	
	def dropEvent(self, event):
		"""
		Event handler for when an item is dropped onto the widget. Handles adding or moving buttons.
		"""
		pos_in_widget = event.pos()
		target_index  = self.main_layout.indexOf(self.childAt(pos_in_widget))

		mime_data     = event.mimeData()
		text          = event.mimeData().text()

		if mime_data.hasText():
			if self.dragged_button:
				old_index = self.main_layout.indexOf(self.dragged_button) # Move an existing button
				self.main_layout.takeAt(old_index)  # Remove from current position
				self.main_layout.insertWidget(self.placeholder_index, self.dragged_button)  # Insert to a new position
				
				self.dragged_button.setVisible(True)
				self.dragged_button = None
			else:
				# Create a new button if dragged_button is not set
				new_button = self.add_button(text)
				if new_button:
					self.main_layout.insertWidget(self.placeholder_index, new_button)
			
			self.parent().parent().parent().set_state_saveButton(True)
			self.placeholder.hide()
			self.placeholder_index = None
			event.acceptProposedAction()
			
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
	
	def __init__(self, step_size = 40, parent = None):
		super(CustemQScrollBar, self).__init__(parent)
		
		self.setStyleSheet(self.scroll_style)
		self.step_size = step_size
	
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
		
		