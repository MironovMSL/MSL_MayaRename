try:
	# Qt5
	from PySide2 import QtCore
	from PySide2 import QtGui
	from PySide2 import QtWidgets
	from shiboken2 import wrapInstance
except:
	# Qt6
	from PySide6 import QtCore
	from PySide6 import QtWidgets
	from PySide6 import QtGui
	from shiboken6 import wrapInstance

import maya.cmds as cmds
import os

root_ = os.path.dirname(__file__)


class RuleTopPanel(QtWidgets.QWidget):

	signal_ListVisibility = QtCore.Signal()
	signal_RuleRun = QtCore.Signal()
	signal_RuleFix = QtCore.Signal()

	def __init__(self, label="Test label"):
		super(RuleTopPanel, self).__init__()
		self.rule_label = label

		self.setup_ui()

	def setup_ui(self):
		# widget Properties
		self.setMinimumWidth(290)
		self.setFixedHeight(40)

		# srt background color
		self.bg = 90
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(self.backgroundRole(), QtGui.QColor(self.bg, self.bg, self.bg))
		self.setPalette(palette)

		# add main layout
		self.main_layout = QtWidgets.QHBoxLayout()
		self.setLayout(self.main_layout)

		# add label
		self.label = QtWidgets.QLabel(self.rule_label)
		self.main_layout.addWidget(self.label)

		# add start button
		self.btn_run = QtWidgets.QPushButton()
		self.btn_run.setIcon(QtGui.QIcon(os.path.join(root_,"resources", "start.svg")))
		self.btn_run.setMaximumWidth(25)
		self.btn_run.clicked.connect(self.on_button_run_clicked)
		self.main_layout.addWidget(self.btn_run)

		# add fix button
		self.btn_fix = QtWidgets.QPushButton()
		self.btn_fix.setIcon(QtGui.QIcon(os.path.join(root_,"resources", "fix.svg")))
		self.btn_fix.setMaximumWidth(25)
		self.btn_fix.clicked.connect(self.on_button_fix_clicked)
		self.main_layout.addWidget(self.btn_fix)

	def on_button_run_clicked(self):
		self.signal_RuleRun.emit()

	def on_button_fix_clicked(self):
		self.signal_RuleFix.emit()

	def set_label(self, text="test"):
		self.rule_label = text
		self.label.setText(text)

	def mouseReleaseEvent(self, event):
		self.signal_ListVisibility.emit()


