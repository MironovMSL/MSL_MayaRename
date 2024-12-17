from socket import create_connection

try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore


from MSL_MayaRename.core.resources import Resources
import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class CustomQSliderWidget(QtWidgets.QSlider):

	wheelScrolled = QtCore.Signal(int)

	def __init__(self, position, range=[], parent=None):
		super(CustomQSliderWidget, self).__init__(parent)
		
		# Module----------------------
		self.resources = Resources.get_instance()
		# Attribute----------------------
		self.letter        = self.resources.config.get_variable("startup", "letter", "", str)
		self.range         = range
		self.position      = position
		self.current_value = self.value()
		self.tooltip = f"Position of letters: {self.current_value}"
		# Setting ------------------------
		self.setOrientation(QtCore.Qt.Horizontal)
		self.setRange(self.range[0], self.range[1])
		self.setVisible(True)
		self.setEnabled(bool(self.letter))
		self.setToolTip(self.tooltip)
		self.setValue(self.position)

		# Run function ------------------------
		self.create_connections()

	def wheelEvent(self, event):
		"""We process the mouse wheel scrolling and generate a signal"""
		delta = event.angleDelta().y() // 120
		self.wheelScrolled.emit(delta)

	def create_connections(self):
		self.valueChanged.connect(self.on_changed_slider_value)

	def on_changed_slider_value(self, value):
		self.tooltip = f"Position of letters: {value}"
		self.setToolTip(self.tooltip)


