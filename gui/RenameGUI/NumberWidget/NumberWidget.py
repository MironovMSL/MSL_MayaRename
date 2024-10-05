from sys import prefix

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

		self.resoures = Resources.get_instance()
		self.FixedHeight = 25
		self.maxRange = 20

		self.setFixedHeight(self.FixedHeight)

		self.create_Widgets()
		self.create_layouts()
		self.create_connections()

	def create_Widgets(self):
		# add CustomQSpinbox
		# self.start = self.resoures.config.set_variable(section="startup", var_name="start_number")

		start = self.resoures.config.get_variable("startup", "start_number", 1)
		pading = self.resoures.config.get_variable("startup", "padding_number", 2)

		self.number_start = CustomQSpinbox(55,25, start, [0, 100], "Start: ")
		self.number_padding = CustomQSpinbox(50, 25,pading, [1, 9], "Pad: ")

		# add QSlider10
		self.index_slider = CustomQSliderWidget([0, self.maxRange])

		self.index_SpinBox = CustomQSpinbox(25, 25, 0, [self.index_slider.minimum(), self.index_slider.maximum()], "")

	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.main_layout.addWidget(self.number_start)
		self.main_layout.addWidget(self.number_padding)
		self.main_layout.addWidget(self.index_slider)
		self.main_layout.addWidget(self.index_SpinBox)

	def create_connections(self):
		pass
		# self.number_start.valueChanged.connect(self.set_number_text)
		# self.number_padding.valueChanged.connect(self.set_number_text)
		self.index_slider.sliderMoved.connect(self.slider_move_text)
		self.index_SpinBox.valueChanged.connect(self.spinBox_value)

	def get_spinBox_value(self, v):
		print(f"TODO spinbix value{v}")

	def slider_move_text(self, value):
		self.index_SpinBox.setValue(value)

	def spinBox_value(self, value):
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
