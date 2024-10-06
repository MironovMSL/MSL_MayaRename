from sys import prefix

from maya.app.renderSetup.model.plug import value

try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore


from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.gui.RenameGUI.NumberWidget.CustomQSpinbox import CustomQSpinbox
from MSL_MayaRename.gui.RenameGUI.NumberWidget.CustomQSliderWidget import CustomQSliderWidget
import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class NumberWidget(QtWidgets.QWidget):

	def __init__(self, parent=None):
		super(NumberWidget, self).__init__(parent)

		self.resources = Resources.get_instance()
		self.FixedHeight = 25
		self.maxRange = 20
		self.start = self.resources.config.get_variable("startup", "start_number", 1)
		self.pading = self.resources.config.get_variable("startup", "padding_number", 2)
		self.position = self.resources.config.get_variable("startup", "position_number", 0)

		self.setFixedHeight(self.FixedHeight)

		self.create_Widgets()
		self.create_layouts()
		self.create_connections()

	def create_Widgets(self):
		# add CustomQSpinbox
		self.number_start = CustomQSpinbox(55,25, self.start, [0, 100], "Start: ", "Starting number")
		self.number_padding = CustomQSpinbox(50, 25,self.pading, [1, 9], "Pad: ", "Padding number")
		# add CustomQSliderWidget
		self.index_slider = CustomQSliderWidget(self.position,[0, self.maxRange])
		# add CustomQSpinbox
		self.index_SpinBox = CustomQSpinbox(25, 25, self.position, [self.index_slider.minimum(), self.index_slider.maximum()], "","Position of number")

	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.main_layout.addWidget(self.number_start)
		self.main_layout.addWidget(self.number_padding)
		self.main_layout.addWidget(self.index_slider)
		self.main_layout.addWidget(self.index_SpinBox)

	def create_connections(self):

		self.index_slider.wheelScrolled.connect(self.on_wheel_scrolled)
		self.number_start.valueChanged.connect(self.set_number_text)
		self.number_padding.valueChanged.connect(self.set_number_text)
		self.index_slider.sliderMoved.connect(self.on_slider_move_value)
		self.index_SpinBox.valueChanged.connect(self.on_spinBox_value)

	def set_state_from_number_mode(self, state):
		# signal from number Button to  RenameGUI to NumberWidget (here)
		self.number_start.setReadOnly(not state)
		self.number_padding.setReadOnly(not state)
		self.index_slider.setEnabled(state)
		self.index_SpinBox.setReadOnly(not state)

	def on_wheel_scrolled(self, delta):
		"""Processing the signal wheelScrolled"""
		current_value = self.index_slider.value()
		step = 1  # Step change value

		if delta > 0:# Update the slider value depending on the scroll direction
			self.index_slider.setValue(current_value + step)
		else:
			self.index_slider.setValue(current_value - step)

		new_value = self.index_slider.value()
		self.index_SpinBox.setValue(new_value)

	def on_slider_move_value(self, value):
		self.index_SpinBox.setValue(value)

	def on_spinBox_value(self, value):
		value_slider = self.index_slider.value()

		# if value_slider != value:
		# 	text = self.lineEdit_rename.text()
		# 	Number = self.NumberText
		# 	start = self.Start_index_Number
		# 	end = start + len(Number)
		# 	left_text = text[:start]
		# 	right_text = text[end:]
		#
		# 	# delete number in text: [left_text][right_text]  del [Number]
		# 	New_Text = left_text + right_text
		#
		# 	# Move number in text: [left_text][Number][right_text]
		# 	number_move = New_Text[:value] + Number + New_Text[value:]
		# 	self.lineEdit_rename.setText(number_move)
		#
		# 	# Save value
		# 	self.oldTextLine = number_move
		# 	self.Start_index_Number = value
		# 	self.lineEdit_rename.setCursorPosition(value)

			# print("[{0}][{2}][{1}] value = {3}".format(New_Text[:value], New_Text[value:],Number, value))

		self.index_slider.setValue(value)

	def set_number_text(self):

		# if self.AnimCheckBox.isChecked():
		# 	Number = self.NumberText
		# else:
		# Number = ""

		# text = self.lineEdit_rename.text()
		# text = ""
		# old_text = self.oldTextLine
		# start = self.Start_index_Number
		# end = start + len(Number)
		# left_text = old_text[:start]
		# right_text = old_text[end:]

		padding = self.number_padding.value()

		self.number_start.setRange(0, (pow(10, padding)))

		number_start = self.number_start.value()

		Number = ("0" * (padding - len(str(number_start)))) + str(number_start)

		# if text:
		# 	NewText = left_text + Number + right_text
		#
		# 	self.lineEdit_rename.setText(NewText)
		# 	self.lineEdit_rename.setCursorPosition(start)
		#
		# 	self.oldTextLine = NewText

		self.NumberText = Number
		# print(self.NumberText)

		# print("[{0}][{2}][{1}] Range = {3} {4}".format(left_text, right_text, Number, self.maxRange, Delete_number))

