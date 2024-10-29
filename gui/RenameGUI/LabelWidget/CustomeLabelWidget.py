try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore


class CustomeLabelWidget(QtWidgets.QLabel):

	itLabelName = QtCore.Signal(str)

	def __init__(self,parent=None):
		super(CustomeLabelWidget, self).__init__(parent)
		# Attribute---------------------------
		self.tooltip  = f"Display selected name and display change name"
		self.color_rename = ""
		self.selected_object = "Select object"
		# style----------------------------
		self.default_style = "font-weight: normal;"
		self.hover_style = "font-size: 10pt; font-weight: bold;"
		self.enter_style = "font-size: 9pt; font-style: italic;"
		# Setting---------------------------
		self.setText(self.selected_object)
		self.setToolTip(self.tooltip)
		self.setAlignment(QtCore.Qt.AlignCenter)
		self.setStyleSheet(self.default_style)
		# Run functions ---------------------------
		self.create_connections()

	def create_connections(self):
		pass

	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		self.setStyleSheet(self.enter_style)
		self.setText(self.selected_object)
		super().enterEvent(event)

	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		self.setStyleSheet(self.default_style)
		if self.color_rename:
			self.setText(self.color_rename)
		else:
			self.setText(self.selected_object)
		super().leaveEvent(event)

	def mousePressEvent(self, event):
		if self.selected_object != "Select object":
			self.setStyleSheet(self.hover_style)
			self.setText(self.selected_object)
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		if self.rect().contains(event.pos()):
			if self.selected_object != "Select object":
				self.setStyleSheet(self.default_style)
				self.setText(self.selected_object)
				self.itLabelName.emit(self.selected_object)
		super().mouseReleaseEvent(event)

	def set_rename_color(self,text, prefix, left, X, mid, Y, right, suffix):
		"""
	    Sets the color and formatting of the text for the element, based on the provided parameters.
	    """

		size   = 12
		colors = {
			'prefix': '#FF6347',  # Tomato
			'left':   '#ffffff',  # White
			'X':      '#1E90FF',  # Dodger Blue
			'mid':    '#ffffff',  # White
			'Y':      '#32CD32',  # Lime Green
			'right':  '#ffffff',  # White
			'suffix': '#DC143C'   # Crimson
		}

		if text:
			self.color_rename = (
	            f'<span style="color: {colors["prefix"]}; font-size: {size}px;">{prefix}</span>'
	            f'<span style="color: {colors["left"]}; font-size: {size}px;">{left}</span>'
	            f'<span style="color: {colors["X"]}; font-size: {size}px;">{X}</span>'
	            f'<span style="color: {colors["mid"]}; font-size: {size}px;">{mid}</span>'
	            f'<span style="color: {colors["Y"]}; font-size: {size}px;">{Y}</span>'
	            f'<span style="color: {colors["right"]}; font-size: {size}px;">{right}</span>'
	            f'<span style="color: {colors["suffix"]}; font-size: {size}px;">{suffix}</span>'
	        )
			self.setText(self.color_rename)
		else:
			self.color_rename = ""
			self.setText(self.selected_object)

	def update_selection(self, name):
		"""
		Updates the selected object and sets the text in the element.
		"""
		if name:
			self.selected_object = name[0].split("|")[-1]
		else:
			self.selected_object = "Select object"

		if not self.color_rename:
			self.setText(self.selected_object)