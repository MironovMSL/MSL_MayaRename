try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class LetterWidget(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(LetterWidget, self).__init__(parent)

		self.FixedHeight = 25
		self.NameHolder = "Letter"

		self.setFixedHeight(self.FixedHeight)

		self.create_Widgets()
		self.create_layouts()
		self.create_connections()

	def create_Widgets(self):

		self.leter_lineEditor = QtWidgets.QLineEdit()
		self.leter_lineEditor.setPlaceholderText(self.NameHolder)
		self.leter_lineEditor.setFixedWidth(133)

		self.index_slider = QtWidgets.QSlider()
		self.index_slider.setOrientation(QtCore.Qt.Horizontal)

		self.index_SpinBox = QtWidgets.QSpinBox()
		self.index_SpinBox.setFixedSize(40, 25)


	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.main_layout.addWidget(self.leter_lineEditor)
		self.main_layout.addWidget(self.index_slider)
		self.main_layout.addWidget(self.index_SpinBox)

	def create_connections(self):
		pass
		# self.number_start.valueChanged.connect(self.set_number_text)
		# self.number_padding.valueChanged.connect(self.set_number_text)
		# self.index_slider.sliderMoved.connect(self.slider_move_text)
		# self.index_SpinBox.valueChanged.connect(self.spinBox_value)
		# self.AnimCheckBox.toggled.connect(self.state_number)