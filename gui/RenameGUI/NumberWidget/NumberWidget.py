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

	new_number_Signal = QtCore.Signal(int, int, str)
	new_position_Signal = QtCore.Signal(int)

	def __init__(self, parent=None):
		super(NumberWidget, self).__init__(parent)
		# Attribute----------------------
		self.FixedHeight = 25
		self.resources   = Resources.get_instance()
		self.QSettings   = QtCore.QSettings(self.resources.config_path, QtCore.QSettings.IniFormat)
		self.maxRange    = 0
		self.start       = self.QSettings.value("startup/start_number", 1, int)
		self.pading      = self.QSettings.value("startup/padding_number", 2, int)
		self.position    = self.QSettings.value("startup/position_number", 0, int)

		# Setting ------------------------
		self.setFixedHeight(self.FixedHeight)

		# Run function ------------------------
		self.create_Widgets()
		self.create_layouts()
		self.create_connections()

	def create_Widgets(self):
		# add CustomQSpinbox
		self.number_start = CustomQSpinbox(55,25, self.start, [0, 100], "Start: ", "Starting number")
		self.number_padding = CustomQSpinbox(50, 25,self.pading, [1, 9], "Pad: ", "Padding number")
		# add CustomQSliderWidget
		self.pos_num_slider = CustomQSliderWidget(self.position,[0, self.maxRange])
		# add CustomQSpinbox
		self.pos_num_spinbox = CustomQSpinbox(25, 25, self.position, [self.pos_num_slider.minimum(), self.pos_num_slider.maximum()], "","Position of number")

	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.main_layout.addWidget(self.number_start)
		self.main_layout.addWidget(self.number_padding)
		self.main_layout.addWidget(self.pos_num_slider)
		self.main_layout.addWidget(self.pos_num_spinbox)


	def create_connections(self):

		self.number_start.valueChanged.connect(self.update_valueChanged_number)
		self.number_padding.valueChanged.connect(self.update_valueChanged_number)
		self.pos_num_slider.wheelScrolled.connect(self.on_wheel_scrolled)
		self.pos_num_slider.sliderMoved.connect(self.on_slider_move_value)
		self.pos_num_spinbox.valueChanged.connect(self.on_spinBox_value)

	def set_state_from_number_mode(self, state):
		# signal from number Button to  RenameGUI to NumberWidget (here)
		self.number_start.setReadOnly(not state)
		self.number_padding.setReadOnly(not state)
		self.pos_num_slider.setEnabled(state)
		self.pos_num_spinbox.setReadOnly(not state)

	def on_wheel_scrolled(self, delta):
		"""Processing the signal wheelScrolled"""
		current_value = self.pos_num_slider.value()
		step = 1  # Step change value

		if delta > 0:# Update the slider value depending on the scroll direction
			self.pos_num_slider.setValue(current_value + step)
		else:
			self.pos_num_slider.setValue(current_value - step)

		new_value = self.pos_num_slider.value()
		self.pos_num_spinbox.setValue(new_value)

	def on_slider_move_value(self, value):
		self.pos_num_spinbox.setValue(value)

	def on_spinBox_value(self, value):
		value_slider = self.pos_num_slider.value()
		# self.pos_num_slider.setValue(value)
		self.new_position_Signal.emit(value)

	def update_valueChanged_number(self):

		padding_number = self.number_padding.value()
		start_number   = self.number_start.value()
		number         = ("0" * (padding_number - len(str(start_number)))) + str(start_number)

		self.number_start.setRange(0, (pow(10, padding_number)))

		# TODO delete QSettings and make QSettings when app close.
		self.QSettings.setValue("startup/start_number", start_number)
		self.QSettings.setValue("startup/padding_number", padding_number)
		self.QSettings.setValue("startup/number", number)

		self.new_number_Signal.emit(start_number, padding_number, number)



