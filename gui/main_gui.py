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

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.common import log
from MSL_MayaRename.gui.ruleWidget.ruleWidget import RuleWidget
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import sys
import os
import maya.cmds as cmds



class ValidatorGui(MayaQWidgetDockableMixin, QtWidgets.QDockWidget):

	def __init__(self):
		super(ValidatorGui, self).__init__()
		self.resource: Resources = Resources.get_instance()
		self.setup_ui()

	def setup_ui(self):
		self.setMinimumWidth(420)
		self.setMinimumHeight(500)
		self.setWindowTitle("Validator")
		self.setObjectName("mayaSceneValidatorID")
		self.setDockableParameters(width=420)

		# main layout
		self.main_wiget = QtWidgets.QWidget()
		self.setWidget(self.main_wiget)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)
		self.main_layout.setSpacing(20)
		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_wiget.setLayout(self.main_layout)

		# top panel

		self.buttons_layout = QtWidgets.QHBoxLayout()
		self.buttons_layout.setSpacing(5)
		self.buttons_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.addLayout(self.buttons_layout)

		# button run
		self.button_run = QtWidgets.QPushButton("Start Validator")
		# self.button_run.setMaximumWidth(32)
		self.button_run.setFixedHeight(32)
		self.button_run.clicked.connect(self.run_validator)
		self.buttons_layout.addWidget(self.button_run)

		# button fix
		self.button_fix = QtWidgets.QPushButton("Fix Failed Checks")
		# self.button_run.setMaximumWidth(32)
		self.button_fix.setFixedHeight(32)
		self.button_fix.clicked.connect(self.fix_validator)
		self.buttons_layout.addWidget(self.button_fix)

		# combobox presets
		self.combo_presets = QtWidgets.QComboBox()
		self.combo_presets.setFixedHeight(32)
		self.combo_presets.setMinimumWidth(150)
		self.buttons_layout.addWidget(self.combo_presets)

		for i in self.resource.get_presets():
			preset_name = os.path.basename(i)
			preset_name_no_extention = os.path.splitext(preset_name)[0]
			self.combo_presets.addItem(preset_name_no_extention)
			self.combo_presets.setCurrentText(self.resource.preset_current)

		self.combo_presets.currentTextChanged.connect(self.save_config_preset)

		# scroll area
		self.scrollarea = QtWidgets.QScrollArea()
		self.scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.scrollarea.setWidgetResizable(True)
		self.scrollarea.setMinimumWidth(300)
		self.scrollarea.setFocusPolicy(QtCore.Qt.NoFocus)
		self.scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.scrollarea_area_widget = QtWidgets.QWidget()
		self.scrollarea.setWidget(self.scrollarea_area_widget)
		self.scroll_layout = QtWidgets.QVBoxLayout()
		self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
		self.scroll_layout.setContentsMargins(0, 0, 0, 0,)
		self.scroll_layout.setSpacing(5)
		self.scrollarea_area_widget.setLayout(self.scroll_layout)
		self.main_layout.addWidget(self.scrollarea)

		# test
		for i in range(20):
			b = RuleWidget()
			self.scroll_layout.addWidget(b)

	def save_config_preset(self, text):
		self.resource.save_current_preset(text)
		log(message="config.ini save. New preset is {}".format(text))

	def run_validator(self):
		print("run")

	def fix_validator(self):
		print("fix")



def creat_gui():
	if cmds.workspaceControl("mayaSceneValidatorIDWorkspaceControl", exists=True):
		cmds.deleteUI("mayaSceneValidatorIDWorkspaceControl", control=True)
		cmds.workspaceControlState("mayaSceneValidatorIDWorkspaceControl", remove=1)

	dialog = ValidatorGui()
	dialog.show(dockable=True, area="right", allowedArea="right", floating=True)
	cmds.workspaceControl("mayaSceneValidatorIDWorkspaceControl", e=1,
						  tabToControl=["AttributeEditor", -1],
						  wp="prefferd",
						  iw=420,
						  mw=420,
						  minimumWidth=True)

	10000
