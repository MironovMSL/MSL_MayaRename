try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

import os
import maya.cmds as cmds
from MSL_MayaRename.gui.RenameGUI.LetterWidget.LineEditLetterWidget import LineEditLetterWidget
from MSL_MayaRename.gui.RenameGUI.LetterWidget.CustomQSpinbox import CustomQSpinbox
from MSL_MayaRename.gui.RenameGUI.LetterWidget.CustomQSliderWidget import CustomQSliderWidget

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator

root_ = os.path.dirname(__file__)

class LetterWidget(QtWidgets.QWidget):

	itEditLetter = QtCore.Signal(str, bool)
	itletPosition = QtCore.Signal(int, str)

	def __init__(self, parent=None):
		super(LetterWidget, self).__init__(parent)
		# Attribute----------------------
		# self.FixedHeight = 25
		self.resources = Resources.get_instance()
		self.QSettings = QtCore.QSettings(self.resources.config_path, QtCore.QSettings.IniFormat)
		# self.maxRange = 0
		# self.start = self.QSettings.value("startup/start_number", 1, int)
		# self.pading = self.QSettings.value("startup/padding_number", 2, int)
		# self.position = self.QSettings.value("startup/position_number", 0, int)
		self.FixedHeight = 25
		self.NameHolder = "Letter"
		self.maxRange   = 0
		self.position   = 0

		self.letter = self.QSettings.value("startup/letter", "" ,str)
		self.mode_letter = self.QSettings.value("startup/mode_letter", False, bool)




		self.setFixedHeight(self.FixedHeight)

		self.create_Widgets()
		self.create_layouts()
		self.create_connections()

	def create_Widgets(self):

		self.leter_lineEditor = LineEditLetterWidget(self.NameHolder,105,)
		self.leter_lineEditor.AutoComplete_line_edit.setText(self.letter)

		self.pos_let_slider = CustomQSliderWidget(self.position,[0, self.maxRange])

		self.pos_let_spinbox = CustomQSpinbox(25,
		                                      25,
		                                      self.position,
		                                      [self.pos_let_slider.minimum(),
		                                       self.pos_let_slider.maximum()],
		                                      "","Position of letters")

	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.main_layout.addWidget(self.leter_lineEditor)
		self.main_layout.addWidget(self.pos_let_slider)
		self.main_layout.addWidget(self.pos_let_spinbox)
		self.main_layout.addWidget(self.pos_let_spinbox)

	def create_connections(self):
		self.leter_lineEditor.AutoComplete_line_edit.textEdited.connect(self.edit_letter)

		self.pos_let_slider.wheelScrolled.connect(self.on_wheel_scrolled)
		self.pos_let_slider.sliderMoved.connect(self.on_slider_move_value)
		self.pos_let_spinbox.valueChanged.connect(self.on_spinBox_value)


	def on_wheel_scrolled(self, delta):
		"""Processing the signal wheelScrolled"""
		current_value = self.pos_let_slider.value()
		step = 1  # Step change value

		if delta > 0:# Update the slider value depending on the scroll direction
			self.pos_let_spinbox.setValue(current_value + step)
		else:
			self.pos_let_spinbox.setValue(current_value - step)




	def on_slider_move_value(self, value):
		self.pos_let_spinbox.setValue(value)

	def on_spinBox_value(self, value):
		value_slider = self.pos_let_slider.value()
		# self.pos_let_slider.setValue(value)
		self.itletPosition.emit(value, "letter")


	def edit_letter(self, letter):

		if letter:
			if not self.mode_letter:
				self.mode_letter = True
				self.pos_let_slider.setEnabled(True)
				self.pos_let_spinbox.setReadOnly(False)
				self.QSettings.setValue("startup/mode_letter", True)
				print(f"Letter Mode: {'checked' if self.mode_letter else 'unchecked'}: '{letter}'")

		else:
			self.mode_letter = False
			self.pos_let_slider.setEnabled(False)
			self.pos_let_spinbox.setReadOnly(True)
			self.QSettings.setValue("startup/mode_letter", False)
			print(f"Letter Mode: {'checked' if self.mode_letter else 'unchecked'}: '{letter}'")

		self.QSettings.setValue("startup/letter", letter)
		self.itEditLetter.emit(letter,self.mode_letter)


