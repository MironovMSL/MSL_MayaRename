try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources


class CustomPushButton(QtWidgets.QPushButton):
	
	def __init__(self, name="", icon="", parent=None):
		super(CustomPushButton, self).__init__(name, parent)
		# Attribute---------------------------
		self.resoures = Resources.get_instance()
		# Setting---------------------------
		self.setFixedSize(25, 25)
	
		if icon:
			self.icon = self.resoures.get_icon_from_resources(icon)
			self.setIcon(self.icon)
	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(CustomPushButton, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(CustomPushButton, self).leaveEvent(event)