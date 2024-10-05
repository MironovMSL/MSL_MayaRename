try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore


from MSL_MayaRename.core.resources import Resources
import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class CustomQSliderWidget(QtWidgets.QSlider):

	def __init__(self,range=[], parent=None):
		super(CustomQSliderWidget, self).__init__(parent)

		self.resoures    = Resources.get_instance()
		# Attribute----------------------
		self.mode_number = self.resoures.config.get_variable("startup", "mode_number", False)
		self.range       = range

		# Setting ------------------------
		self.setOrientation(QtCore.Qt.Horizontal)
		self.setRange(self.range[0], self.range[1])
		self.setVisible(True)
		self.setEnabled(self.mode_number)