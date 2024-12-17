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
		self.setIcon(self.icon)
		self.setIconSize(QtCore.QSize(25, 25))
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
		print("TODO: set  auto suffix all selected objects ")
	
	def update_selection(self):
		"""
		Updates the current selection of objects in the scene and reflects this in the UI.
		"""
		selection = cmds.ls(selection=True, l=True)
		icon = None
		
		if selection:
			# Проверяем тип первого выбранного объекта
			type_obj = cmds.objectType(selection[0])
			if type_obj == "transform":
				# Ищем шейпы, связанные с трансформом
				shapes = cmds.listRelatives(selection[0], shapes=True, fullPath=True)
				if shapes:
					for shape in shapes:
						# Определяем тип шейпа
						shape_type = cmds.objectType(shape)
						print(f"Шейп: {shape}, Тип: {shape_type}")

						if shape_type == "camera":
							icon = QtGui.QIcon(f":Camera")
						else:
							icon = QtGui.QIcon(f":{shape_type}")
						
				else:
					print(f"У трансформа {selection[0]} нет связанных шейпов.")
					icon = QtGui.QIcon(f":{type_obj}")
			else:
				print(f"Тип выбранного объекта: {type_obj}")
				if type_obj == "joint":
					icon = QtGui.QIcon(f":kinJoint")
				elif type_obj == "camera":
					icon = QtGui.QIcon(f":Camera")
				else:
					icon = QtGui.QIcon(f":{type_obj}")
		else:
			print("Ничего не выделено.")
			
		if icon:
			print(icon)
			self.setIcon(icon)
			self.setIconSize(QtCore.QSize(20, 20))
		else:
			self.setIcon(self.icon)
			self.setIconSize(QtCore.QSize(25, 25))
			
		
		# for obj in object_list:
		# 	if not cmds.objectType(obj, isType="transform"):
		# 		parent_transform = cmds.listRelatives(obj, parent=True, fullPath=True)
		# 		if parent_transform and parent_transform[0] in object_list:
		# 			continue
		#
		# 	filtered_list.append(obj)

	
	# def create_icons(self):
	# 	self.transform_icon = QtGui.QIcon(":transform.svg")
	# 	self.camera_icon = QtGui.QIcon(":Camera.png")
	# 	self.mesh_icon = QtGui.QIcon(":mesh.svg")
	#
	#
	# def update_icon(self, item):
	# 	object_type = "transform"
	#
	# 	if object_type == "transform":
	# 		item.setIcon(0, self.transform_icon)
	# 	elif object_type == "camera":
	# 		item.setIcon(0, self.camera_icon)
	# 	elif object_type == "mesh":
	# 		item.setIcon(0, self.mesh_icon)
	
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
		self.type = self.resoures.config.get_variable("startup", "type_find", "selected", str)
		# Setting---------------------------
		self.setObjectName("PopUpWindow")
		self.setWindowTitle(f"Type options")
		self.setWindowFlags(QtCore.Qt.Popup)
		self.setFixedSize(180, 25)
		
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layout()
		self.create_connections()
		self.set_checked_btn(self.type)
	
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

