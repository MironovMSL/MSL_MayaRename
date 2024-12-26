try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from functools import partial

from MSL_MayaRename.core.resources import Resources
import maya.cmds as cmds


class AutoPrefixButton(QtWidgets.QPushButton):
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
	
	# button AP - auto prefix --> lt_Name rt_Name mid_Name
	# [(lf),(lf,mif),(lf, rf), (lf, mid, rt), (rt), (rt, mid), (mid)]
	
	def __init__(self, parent=None):
		super(AutoPrefixButton, self).__init__(parent)
		# Module---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon              = self.resources.get_icon_from_resources("elk-svgrepo-com.svg")
		self.toolTip           = "Automatically adds short form name prefix such as (lf, mid, rt)."
		self.script_job_number = -1
		# Setting---------------------------
		self.setObjectName("AutoPrefixButtonID")
		self.setFixedSize(25, 25)
		self.setToolTip(self.toolTip)
		self.setStyleSheet(self.Style_btn)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
		self.update_selection()

	
	def create_widgets(self):
		self.lf_widget  = QtWidgets.QWidget()
		self.mid_widget = QtWidgets.QWidget()
		self.rt_widget  = QtWidgets.QWidget()
		# self.pop_up_window = PopUpWindow(self)
	
	def create_layouts(self):
		self.Colorlayout = QtWidgets.QHBoxLayout(self)
		self.Colorlayout.setContentsMargins(0, 0, 0, 0)
		self.Colorlayout.setSpacing(0)
		
		self.Colorlayout.addWidget(self.rt_widget)
		self.Colorlayout.addWidget(self.mid_widget)
		self.Colorlayout.addWidget(self.lf_widget)
		
		
	
	def create_connections(self):
		pass
		# self.customContextMenuRequested.connect(self.show_pop_up_window)
	
	def update_selection(self):
		"""
		Updates the current selection of objects in the scene and reflects this in the UI.
		"""
		combination = [ ]
		selection = cmds.ls(selection=True, l=True)
		
		if selection:
			for obj in selection:
				type_obj = cmds.objectType(obj)
				if type_obj == "transform" or type_obj == "joint":
					position = self.classify_object_position(obj)
					if position not in combination:
						combination.append(position)
		
		self.update_icon(combination = combination)

	

	def update_icon(self, combination = [ ] ):
		if combination:
			if set(["lf"]) == set(combination):
				icon = self.resources.get_icon_from_resources("lf.svg")
			elif set(["lf", "mid"]) == set(combination):
				icon = self.resources.get_icon_from_resources("lf_mid.svg")
			elif set(["lf", "rt"]) == set(combination):
				icon = self.resources.get_icon_from_resources("lf_rf.svg")
			elif set(["lf", "mid", "rt"]) == set(combination):
				icon = self.resources.get_icon_from_resources("lf_mid_rt.svg")
			elif set(["rt"]) == set(combination):
				icon = self.resources.get_icon_from_resources("rt.svg")
			elif set(["rt", "mid"]) == set(combination):
				icon = self.resources.get_icon_from_resources("rt_mid.svg")
			elif set(["mid"]) == set(combination):
				icon = self.resources.get_icon_from_resources("mid.svg")
			size = 15
		else:
			icon = self.icon
			size = 25

			
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(size, size))
	
	def classify_object_position(self, obj_name):
		
		
		position = cmds.xform(obj_name, q=True, t=True, ws=True)
		x_pos = position[0]

		if x_pos < 0:
			return "rt"
		elif x_pos == 0:
			return "mid"
		else:
			return "lf"
	
	def update_position(self):
		# Эта функция будет вызываться при изменении позиции объекта
		print("Объект был перемещен!")
		
		
	def set_script_job_enabled(self, enabled):
		"""
		Enables or disables a script job that monitors selection changes in the Maya scene.
		"""
		if enabled and self.script_job_number < 0:
			self.script_job_number = cmds.scriptJob(event=["SelectionChanged", partial(self.update_selection)], protected=True)
		elif not enabled and self.script_job_number >= 0:
			cmds.scriptJob(kill=self.script_job_number, force=True)
			self.script_job_number = -1

	
	def show_pop_up_window(self, pos):
		"""
		Displays the pop-up window at the position of the button.
		"""
		count = self.pop_up_window.scroll_widget_layout.count()
		if count:
			pop_up_pos = self.mapToGlobal(QtCore.QPoint(0, 25))
			
			self.pop_up_window.move(pop_up_pos)
			self.pop_up_window.show()
	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(AutoPrefixButton, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		self.setStyleSheet(self.Style_btn)
		super(AutoPrefixButton, self).leaveEvent(event)