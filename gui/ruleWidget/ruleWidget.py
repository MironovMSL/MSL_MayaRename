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
from .ruleTopPanel import RuleTopPanel
from .ruleListPanel import RuleListPanel


class RuleWidget(QtWidgets.QWidget):

	signal_validator_run = QtCore.Signal()
	signal_validator_fix = QtCore.Signal()

	def __init__(self, rule_name="name", rule_description="description"):
		super(RuleWidget, self).__init__()

		self.rule_name = rule_name
		self.rule_description = rule_description

		self.setup_ui()

	def setup_ui(self):
		# main layout
		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 5, 0)
		self.setLayout(self.main_layout)

		# add top panel
		self.top_panel = RuleTopPanel(self.rule_name)
		self.top_panel.signal_ListVisibility.connect(self.toggle_list_panel_visibility)
		self.top_panel.signal_RuleRun.connect(self.on_rule_run)
		self.top_panel.signal_RuleFix.connect(self.on_rule_fix)
		self.main_layout.addWidget(self.top_panel)

		# add bottom list panel
		self.list_panel = RuleListPanel()
		self.list_panel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
		self.main_layout.addWidget(self.list_panel)

	def get_rule_name(self):
		return self.rule_name

	def set_rule_name(self, name):
		self.rule_name = name
		# todo set this name to top panel

	def get_rule_description(self):
		return self.rule_description

	def set_rule_description(self, descrioption):
		self.rule_description = descrioption
		# todo set this discription to bottom panel label

	def toggle_list_panel_visibility(self):
		self.list_panel.toggle_visibility()

	def on_rule_run(self):
		self.signal_validator_run.emit()

	def on_rule_fix(self):
		self.signal_validator_fix.emit()
