try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.core.common import *
import os


class CustomeLabelWidget(QtWidgets.QLabel):

	Style_btn = """
	        QPushButton {
	            background-color: rgb(50, 50, 50); /* Темно-серый фон */
	            border-style: outset;
	            border-width: 2px;
	            border-radius: 8px;
	            border-color: rgb(30, 30, 30); /* Темнее границы */
	            font: bold 14px; /* Жирный шрифт */
	            font-family: Arial; /* Шрифт Arial */
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

	        QPushButton:checked {
	            background-color: rgb(80, 120, 80); /* Зеленоватый оттенок при нажатии (состояние check) */
	            border-color: rgb(60, 90, 60); /* Темно-зеленая граница при нажатии */
	            color: rgb(240, 240, 240); /* Белый текст */
	        }

	        QPushButton:checked:hover {
	            background-color: rgb(100, 140, 100); /* Светлее при наведении в состоянии checked */
	            border-color: rgb(80, 110, 80); /* Светлее при наведении в состоянии checked */
	        }
	    """

	def __init__(self,parent=None):
		super(CustomeLabelWidget, self).__init__(parent)
		# Attribute---------------------------
		self.tooltip  = f"Insert selected name. Display change name"
		self.color_rename = "change name"
		self.selected_object = "selected object"
		self.name = '<font color="red">selected</font> and <font color="blue">object</font>.'
		# Setting---------------------------
		self.setText(self.color_rename)
		self.setToolTip(self.tooltip)
		self.setStyleSheet(self.Style_btn)
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
		self.setText(self.color_rename)
		super().leaveEvent(event)

	def mousePressEvent(self, mouse_event):
		print("Mouse Button Pressed")
		self.setStyleSheet(self.hover_style)
		self.setText(self.selected_object)

	def mouseReleaseEvent(self, mouse_event):
		print("Mouse Button Released")
		self.setStyleSheet(self.default_style)
		self.setText(self.selected_object)

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
		else:
			self.color_rename = "change name"

		self.setText(self.color_rename)

