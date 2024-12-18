from maya.cmds import iconTextButton

try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	
from functools import partial

from MSL_MayaRename.core.resources import Resources
import maya.cmds as cmds

class AutoSuffixButton(QtWidgets.QPushButton):
	Style_btn = """
		    QPushButton {
		        background-color: rgb(50, 50, 50); /* Темно-серый фон */
		        border-style: outset;
		        border-width: 2px;
		        border-radius: 8px;
		        border-color: rgb(30, 30, 30); /* Темнее границы */
		        font: normal 12px; /* Жирный шрифт */
		        font-family: Roboto; /* Шрифт Arial  Helvetica, Calibri, Verdana, Tahoma, Segoe UI, Open Sans, Roboto, Source Sans Pro */
		        color: rgb(200, 200, 200); /* Светло-серый текст */
		        padding: 0px; /* Внутренние отступы */
		    }
		    QPushButton:hover {
		        border-color: rgb(70, 70, 70); /* Светло-серая граница при наведении */
		        background-color: rgb(80, 80, 80); /* Более светлый серый при наведении */
		    }
		    QPushButton:pressed {
		        background-color: rgb(30, 30, 30); /* Почти черный при нажатии */
		        border-style: inset; /* Впадение при нажатии */
		        color: rgb(220, 220, 220); /* Почти белый текст при нажатии */
		    }
		"""
	
	def __init__(self, parent=None):
		super(AutoSuffixButton, self).__init__(parent)
		# Module---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon     = self.resources.get_icon_from_resources("crab-svgrepo-com.svg")
		self.toolTip  = "Automatically adds a suffix of a short name shape."
		self.script_job_number = -1
		# Setting---------------------------
		self.setObjectName("AutoSuffixButtonID")
		self.setFixedSize(25, 25)
		self.setToolTip(self.toolTip)
		self.setStyleSheet(self.Style_btn)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_connections()
		self.update_selection()
	
	def create_widgets(self):
		self.pop_up_window = PopUpWindow(self)
	
	def create_connections(self):
		self.clicked.connect(self.set_auto_suffix)
		self.customContextMenuRequested.connect(self.show_pop_up_window)
		# self.pop_up_window.btn_grp.buttonClicked.connect(self.on_button_clicked)
	
	def show_pop_up_window(self, pos):
		"""
		Displays the pop-up window at the position of the button.
		"""
		pop_up_pos = self.mapToGlobal(QtCore.QPoint(0, 25))
		
		self.pop_up_window.move(pop_up_pos)
		self.pop_up_window.show()
	
	def set_auto_suffix(self):
		print(f"TODO: set  auto suffix all selected objects\n{self.type_list}")
		
	
	def update_selection(self):
		"""
		Updates the current selection of objects in the scene and reflects this in the UI.
		"""
		selection = cmds.ls(selection=True, l=True)
		
		self.icon_list = [ ]
		self.size_list = [ ]
		self.type_list = [ ]

		if selection:
			for index, obj in enumerate(selection):
				icon, size, type_obj = self.get_icon(obj)
				if type_obj not in self.type_list:
					self.icon_list.append(icon)
					self.size_list.append(size)
					self.type_list.append(type_obj)
				if index == 0:
					self.set_icon(icon, size)
		else:
			obj = None
			icon, size, type_obj = self.get_icon(obj)
			self.set_icon(icon, size)

	def set_icon(self,icon, size):
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(size, size))
		
	def get_icon(self, obj = None):
		"""
		Determines the appropriate icon and size for a given Maya object.
		"""
		if obj:
			type_obj = cmds.objectType(obj)
			if type_obj == "transform":
				shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
				if shapes:
					for shape in shapes:
						type_obj = cmds.objectType(shape)
						
						if type_obj == "camera":
							icon = QtGui.QIcon(f":Camera")
						else:
							icon = QtGui.QIcon(f":{type_obj}")
						break
				else:
					icon = QtGui.QIcon(f":{type_obj}")
			else:
				if type_obj == "joint":
					icon = QtGui.QIcon(f":kinJoint")
				elif type_obj == "camera":
					icon = QtGui.QIcon(f":Camera")
				else:
					icon = QtGui.QIcon(f":{type_obj}")
					if not icon.availableSizes(): # icon empty
						icon = QtGui.QIcon(f":mayaIcon")
			size = 20
		else:
			type_obj = ""
			icon     = self.icon
			size     = 25

		return icon, size, type_obj
	
	def set_script_job_enabled(self, enabled):
		"""
		Enables or disables a script job that monitors selection changes in the Maya scene.
		"""
		if enabled and self.script_job_number < 0:
			self.script_job_number = cmds.scriptJob(event=["SelectionChanged", partial(self.update_selection)],
			                                        protected=True)
		elif not enabled and self.script_job_number >= 0:
			cmds.scriptJob(kill=self.script_job_number, force=True)
			self.script_job_number = -1
	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(AutoSuffixButton, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		self.setStyleSheet(self.Style_btn)
		super(AutoSuffixButton, self).leaveEvent(event)


class PopUpWindow(QtWidgets.QWidget):
	"""
	Class for creating a pop-up window with options.
	"""
	
	def __init__(self, parent=None):
		super(PopUpWindow, self).__init__(parent)
		# Module---------------------------
		self.resoures = Resources.get_instance()
		# Attribute---------------------------

		# Setting---------------------------
		self.setObjectName("AutoSuffixPopUpWindowID")
		self.setWindowTitle(f"Type options")
		self.setWindowFlags(QtCore.Qt.Popup)
		self.setFixedSize(180, 25)
		
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layout()
		self.create_connections()
	
	def create_widgets(self):
		self.sel = QtWidgets.QRadioButton("selected")
		self.hi = QtWidgets.QRadioButton("hierarchy")
		self.all = QtWidgets.QRadioButton("all")
		
		self.btn_grp = QtWidgets.QButtonGroup()
		self.btn_grp.addButton(self.sel)
		self.btn_grp.addButton(self.hi)
		self.btn_grp.addButton(self.all)
	
	def create_layout(self):
		self.grp_layout = QtWidgets.QHBoxLayout()
		self.grp_layout.addWidget(self.sel)
		self.grp_layout.addWidget(self.hi)
		self.grp_layout.addWidget(self.all)
		self.grp_layout.setContentsMargins(0, 0, 0, 0)
		self.grp_layout.setSpacing(2)
		# self.grp_layout.addStretch()
		
		self.main_layout = QtWidgets.QFormLayout(self)
		self.main_layout.setContentsMargins(2, 2, 2, 2)
		self.main_layout.setSpacing(0)
		
		self.main_layout.addRow("", self.grp_layout)
	
	def create_connections(self):
		pass
	
	def set_checked_btn(self, type):
		self.type = type
		
		if type == "selected":
			self.sel.setChecked(True)
		elif type == "hierarchy":
			self.hi.setChecked(True)
		elif type == "all":
			self.all.setChecked(True)

