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

	itEditLetter = QtCore.Signal(str)
	itletPosition = QtCore.Signal(int, str)
	itShowLetter  = QtCore.Signal(bool)

	def __init__(self, parent=None):
		super(LetterWidget, self).__init__(parent)
		# Module----------------------
		self.resources = Resources.get_instance()
		# Attribute----------------------
		self.letter      = self.resources.config.get_variable("startup", "letter", "", str)
		self.mode_letter = self.resources.config.get_variable("startup", "mode_letter", False, bool)
		self.FixedHeight = 25
		self.NameHolder  = "Letter"
		self.maxRange    = 0
		self.position    = 0
		# Setting---------------------------
		self.setFixedHeight(self.FixedHeight)
		if not self.mode_letter:
			self.setVisible(self.mode_letter)

		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
		

	def create_widgets(self):
		self.time = QtCore.QTimer()
		self.leter_lineEditor = LineEditLetterWidget(self.NameHolder,105,)
		self.leter_lineEditor.AutoComplete_line_edit.setText(self.letter)
		self.pos_let_slider = CustomQSliderWidget(self.position,[0, self.maxRange])
		self.pos_let_spinbox = CustomQSpinbox(25,25, self.position,[self.pos_let_slider.minimum(), self.pos_let_slider.maximum()],"","Position of letters")

	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.main_layout.addWidget(self.leter_lineEditor)
		self.main_layout.addWidget(self.pos_let_slider)
		self.main_layout.addWidget(self.pos_let_spinbox)


	def create_connections(self):
		self.leter_lineEditor.AutoComplete_line_edit.textEdited.connect(self.edit_letter)
		self.pos_let_slider.wheelScrolled.connect(self.on_wheel_scrolled)
		self.pos_let_slider.sliderMoved.connect(self.on_slider_move_value)
		self.pos_let_spinbox.valueChanged.connect(self.on_spinBox_value)
		self.time.timeout.connect(self.emit_letter)

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
		self.itletPosition.emit(value, "letter")

	def set_state_from_letter_mode(self, state):
		self.mode_letter = state
		self.setVisible(state)
		self.parent().RenameButton.update_size_btn(state)

		self.leter_lineEditor.setEnabled(state)

		self.resources.config.set_variable("startup", "mode_letter", state)

		self.time.start(20)

	def emit_letter(self):
		self.time.stop()
		self.itShowLetter.emit(self.mode_letter)
	
	def edit_letter(self, letter):
		self.resources.config.set_variable("startup", "letter", letter)
		if letter:
			self.pos_let_slider.setEnabled(True)
			self.pos_let_spinbox.setReadOnly(False)
		else:
			self.pos_let_slider.setEnabled(False)
			self.pos_let_spinbox.setReadOnly(True)
		self.itEditLetter.emit(letter)
