try:
	# Qt5
	from PySide2 import QtCore
	from PySide2 import QtGui
	from PySide2 import QtWidgets
	from shiboken2 import wrapInstance

	from PySide2.QtWidgets import QAction
except:
	# Qt6
	from PySide6 import QtCore
	from PySide6 import QtGui
	from PySide6 import QtWidgets
	from shiboken6 import wrapInstance

	from PySide6.QtGui import QAction

import sys

from functools import partial

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.core.common import *
import os
import maya.OpenMayaUI as omui
import maya.cmds as cmds


class CustomeLabelWidget(QtWidgets.QLabel):

	itLabelName = QtCore.Signal(str)

	def __init__(self,parent=None):
		super(CustomeLabelWidget, self).__init__(parent)
		# Attribute---------------------------
		self.tooltip  = f"Display selected name and display change name"
		self.color_rename = ""
		self.selected_object = "Select object"
		# Setting---------------------------
		self.setText(self.selected_object)
		self.setToolTip(self.tooltip)
		self.setAlignment(QtCore.Qt.AlignCenter)
		# ---------------------------
		self.default_style = "font-weight: normal;"  # Обычный текст
		self.hover_style = "font-size: 10pt; font-weight: bold;"
		self.enter_style = "font-size: 9pt; font-style: italic;"

		self.setStyleSheet(self.default_style)

		Font = QtGui.QFont("Arial", 10, QtGui.QFont.Normal)

		self.create_connections()

	def create_connections(self):
		pass

	def enterEvent(self, event):
		self.setStyleSheet(self.enter_style)
		self.setText(self.selected_object)
		super().enterEvent(event)

	def leaveEvent(self, event):
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
		size = 12
		if text:
			self.color_rename = (
							    f'<span style="color: #FF6347; font-size: {size}px;">{prefix}</span>'   # Префикс
							    f'<span style="color: #ffffff; font-size: {size}px;">{left}</span>'                     # Левый текст
							    f'<span style="color: #1E90FF; font-size: {size}px;">{X}</span>'        # Символ X
							    f'<span style="color: #ffffff; font-size: {size}px;">{mid}</span>'                      # Средний текст
							    f'<span style="color: #32CD32; font-size: {size}px;">{Y}</span>'        # Символ Y
							    f'<span style="color: #ffffff; font-size: {size}px;">{right}</span>'                    # Правый текст
							    f'<span style="color: #DC143C; font-size: {size}px;">{suffix}</span>'   # Суффикс
							)
			self.setText(self.color_rename)
		else:
			self.color_rename = ""
			self.setText(self.selected_object)

	def update_selection(self, name):
		if name:
			self.selected_object = name[0].split("|")[-1]
		else:
			self.selected_object = "Select object"

		if not self.color_rename:
			self.setText(self.selected_object)
