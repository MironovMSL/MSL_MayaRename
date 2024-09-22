try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class NumberWidget(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(NumberWidget, self).__init__(parent)

		self.FixedHeight = 25
		self.maxRange = 0

		self.setFixedHeight(self.FixedHeight)

		self.create_Widgets()
		self.create_layouts()
		self.create_connections()

	def create_Widgets(self):

		self.number_start = QtWidgets.QSpinBox()
		self.number_start.setPrefix("Start: ")
		self.number_start.setValue(1)
		self.number_start.setRange(0, 100)
		self.number_start.setFixedSize(68, 25)
		# self.number_start.setReadOnly(True)

		self.number_padding = QtWidgets.QSpinBox()
		self.number_padding.setPrefix("Pad: ")
		self.number_padding.setValue(2)
		self.number_padding.setRange(1, 9)
		self.number_padding.setFixedSize(65, 25)
		# self.number_padding.setReadOnly(True)

		self.index_slider = QtWidgets.QSlider()
		self.index_slider.setOrientation(QtCore.Qt.Horizontal)
		# self.index_slider.setMaximumWidth(100)
		# self.index_slider.setRange(0, self.maxRange)
		self.index_slider.setVisible(1)

		self.index_SpinBox = QtWidgets.QSpinBox()
		self.index_SpinBox.setFixedSize(40, 25)
		# self.index_SpinBox.setRange(self.index_slider.minimum(), self.index_slider.maximum())
		# self.index_SpinBox.setReadOnly(True)

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
		# self.index_slider.sliderMoved.connect(self.slider_move_text)
		# self.index_SpinBox.valueChanged.connect(self.spinBox_value)
		# self.AnimCheckBox.toggled.connect(self.state_number)