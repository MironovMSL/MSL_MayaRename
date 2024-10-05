try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.core.common import *
import os


class RemoveButtonWidget(QtWidgets.QPushButton):

	def __init__(self, name="", width=25, height=25, icon="", parent=None):
		super(RemoveButtonWidget, self).__init__(name, parent)


		self.width    = width
		self.height   = height
		self.resoures = Resources.get_instance()

		if icon:
			self.icon     = self.resoures.get_icon_from_resources(icon)
			self.setIcon(self.icon)
			# self.setIconSize(QtCore.QSize(width, height))

		self.setFixedSize(self.width,self.height)

		self.setStyleSheet("QPushButton { padding: 0px; }")


