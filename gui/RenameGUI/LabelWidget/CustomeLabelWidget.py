try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.core.common import *
import os


class CustomeLabelWidget(QtWidgets.QLabel):

	def __init__(self,parent=None):
		super(CustomeLabelWidget, self).__init__(parent)
		# Attribute---------------------------
		self.tooltip  = f"Display selected name and display change name"
		self.color_rename = ""
		self.selected_object = "selected object"
		# Setting---------------------------
		self.setText(self.selected_object)
		self.setToolTip(self.tooltip)
		self.setAlignment(QtCore.Qt.AlignCenter)
		# ---------------------------
		self.default_style = "font-weight: normal;"  # Обычный текст
		self.hover_style = "font-size: 10pt; font-weight: bold;"

		self.setStyleSheet(self.default_style)

		Font = QtGui.QFont("Arial", 10, QtGui.QFont.Normal)

		self.create_connections()

	def create_connections(self):
		pass

	def enterEvent(self, event):
		print("enter event")
		self.setStyleSheet(self.default_style)
		self.setText(self.selected_object)
		super().enterEvent(event)

	def leaveEvent(self, event):
		print("leave event")
		self.setStyleSheet(self.default_style)

		if self.color_rename:
			self.setText(self.color_rename)
		else:
			self.setText(self.selected_object)

		super().leaveEvent(event)

	def mousePressEvent(self, event):
		print("Mouse Button Pressed")
		self.setStyleSheet(self.hover_style)
		self.setText(self.selected_object)

		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		print("Mouse Button Released")
		self.setStyleSheet(self.default_style)
		self.setText(self.selected_object)

		super().mouseReleaseEvent(event)

	def set_rename_color(self,text, prefix, left, X, mid, Y, right, suffix):
		size = 14
		if text:
			self.color_rename = (
							    f'<span style="color: #FF6347; font-size: {size}px;">{prefix}</span>'   # Префикс
							    f'<span style="font-size: {size}px;">{left}</span>'                     # Левый текст
							    f'<span style="color: #1E90FF; font-size: {size}px;">{X}</span>'        # Символ X
							    f'<span style="font-size: {size}px;">{mid}</span>'                      # Средний текст
							    f'<span style="color: #32CD32; font-size: {size}px;">{Y}</span>'        # Символ Y
							    f'<span style="font-size: {size}px;">{right}</span>'                    # Правый текст
							    f'<span style="color: #DC143C; font-size: {size}px;">{suffix}</span>'   # Суффикс
							)
			self.setText(self.color_rename)
		else:
			self.color_rename = ""
			self.setText(self.selected_object)


