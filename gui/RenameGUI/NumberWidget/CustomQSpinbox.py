try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore


from MSL_MayaRename.core.resources import Resources
import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class CustomQSpinbox(QtWidgets.QSpinBox):
	Style_spinBox = """
			    QSpinBox {
			        background-color: rgb(40, 40, 40);  /* Темно-серый фон */
			        border: 2px solid rgb(70, 70, 70);  /* Темная серая граница */
			        border-radius: 8px;

			        color: rgb(220, 220, 220);          /* Светло-серый текст */
			    }

			    QSpinBox::up-button {
			        subcontrol-origin: border;
			        subcontrol-position: top right;  /* Кнопка "вверх" справа */
			        width: 16px;                     /* Ширина кнопки */
			        background-color: rgb(50, 50, 50);  /* Темно-серый фон */
			        border-left: 1px solid rgb(70, 70, 70);  /* Разделительная граница */
			    }

			    QSpinBox::up-button:hover {
			        background-color: rgb(60, 60, 60);  /* Светлее при наведении */
			    }

			    QSpinBox::up-button:pressed {
			        background-color: rgb(30, 30, 30);  /* Темнее при нажатии */
			    }

			    QSpinBox:hover {
			        border: 2px solid rgb(100, 100, 100);  /* Светлая граница при наведении */
			    }

			    QSpinBox:focus {
			        border: 2px solid rgb(150, 150, 150);  /* Светлая граница при фокусе */
			        background-color: rgb(45, 45, 45);     /* Немного светлее при фокусе */
			    }
			"""
	def __init__(self,width=55, height=25, start_Value=int,range=[], prefix="", tooltip="", parent=None):
		super(CustomQSpinbox, self).__init__(parent)

		# Attribute----------------------
		self.resoures    = Resources.get_instance()
		self.mode_number = self.resoures.config.get_variable("startup", "mode_number", False)
		self.width       = width
		self.height      = height
		self.prefix      = prefix
		self.range       = range
		self.start_Value = start_Value
		self.tooltip     = tooltip
		self.name        = ""

		# Check tooltip----------------------
		if self.tooltip == "Starting number":
			self.name = self.tooltip
			self.tooltip = f"{self.tooltip} : {start_Value}"

		elif self.tooltip == "Padding number":
			self.name = self.tooltip
			pading = lambda: "0" * start_Value
			self.tooltip = f"{self.tooltip} : {start_Value} = {pading()}"

		elif  self.tooltip == "Position of number":
			self.name = self.tooltip
			self.tooltip = f"{self.tooltip} : {start_Value}"

		# Setting ------------------------
		self.setFixedSize(width, height)
		self.setPrefix(self.prefix)
		self.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
		self.setValue(self.start_Value)
		self.setRange(self.range[0], self.range[1])
		self.setReadOnly(not self.mode_number)
		self.setStyleSheet(self.Style_spinBox)
		self.setToolTip(self.tooltip)

		self.create_connections()

	def create_connections(self):
		self.valueChanged.connect(self.on_changed_spinbox_value)

	def on_changed_spinbox_value(self,value):
		if self.name == "Starting number":
			self.tooltip = f"{self.name} : {value}"
		elif self.name == "Padding number":
			pading = lambda: "0" * value
			self.tooltip = f"{self.name} : {value} = {pading()}"
		elif self.name == "Position of number":
			self.tooltip = f"{self.name} : {value}"

		self.setToolTip(self.tooltip)
