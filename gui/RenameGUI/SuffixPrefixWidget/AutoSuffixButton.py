from cProfile import label

from maya.cmds import iconTextButton, select

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
		count = self.pop_up_window.scroll_widget_layout.count()
		if count:
			pop_up_pos = self.mapToGlobal(QtCore.QPoint(0, 25))
			
			self.pop_up_window.move(pop_up_pos)
			self.pop_up_window.show()
	
	def set_auto_suffix(self):
		selection = cmds.ls(selection=True, l=True)
		if selection:
			filtered_list = self.parent().parent().FindReplaceWidget.remove_shapes_from_transforms(selection)
			
			for obj in filtered_list:
				type_obj = self.get_type_object(obj)
				suffix   = self.resources.config.get_variable("auto_suffix", type_obj, "", str)
				path_to_obj, obj_short_name = self.parent().parent().get_short_name(obj)
				
				print(f"{type_obj:<20}: {obj_short_name:<20}: {suffix}")
				
				if not suffix:
					continue

				if obj_short_name[len(obj_short_name) - len(suffix):] == suffix:
					continue
				
				new_obj_short_name = obj_short_name + suffix
				obj_rename         = cmds.rename(obj, new_obj_short_name)
				
				new_path_to_obj, new_obj_short_name = self.parent().parent().get_short_name(obj_rename)
				new_obj            = path_to_obj + new_obj_short_name
				
				filtered_list =  self.parent().parent().renameObjectsInHierarchy(filtered_list, obj, new_obj)
			
			self.parent().parent().LabelWidget.update_selection()
			
		else:
			print("It is necessary to select an object.")
		
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
			
		self.pop_up_window.add_content_selected_type(self.type_list, self.icon_list, self.size_list)

	def set_icon(self,icon, size):
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(size, size))
		
	def get_type_object(self, obj):
		type_obj = cmds.objectType(obj)
		if type_obj == "transform":
			shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
			if shapes:
				for shape in shapes:
					type_obj = cmds.objectType(shape)
					break
		return type_obj

	
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
						if not icon.availableSizes():  # icon empty
							icon = QtGui.QIcon(f":default")
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
						icon = QtGui.QIcon(f":default")
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
	scroll_style = """
QScrollBar:vertical {
    background: rgb(10, 10, 10); /* Очень тёмный фон */
    width: 8px; /* Ширина вертикального скроллбара */
    margin: 0px; /* Нет отступов вокруг скроллбара */
}

QScrollBar::handle:vertical {
    background: rgb(50, 50, 50); /* Тёмно-серый, соответствующий фону кнопок */
    border: 1px solid rgb(30, 30, 30); /* Тёмная рамка */
    border-radius: 3px; /* Скругление углов для сглаженности */
    min-height: 20px; /* Минимальная высота */
}

QScrollBar::handle:vertical:hover {
    background: rgb(80, 80, 80); /* Светло-серый при наведении */
    border: 1px solid rgb(70, 70, 70); /* Светлая рамка при наведении */
}

QScrollBar::handle:vertical:pressed {
    background: rgb(30, 30, 30); /* Почти чёрный при нажатии */
    border: 1px solid rgb(20, 20, 20); /* Тёмная рамка при нажатии */
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    width: 0px; /* Нет кнопок "вверх" и "вниз" */
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none; /* Нет дополнительных страниц (не перекрашивать фон) */
}
	"""
	
	def __init__(self, parent=None):
		super(PopUpWindow, self).__init__(parent)
		# Module---------------------------
		self.resoures = Resources.get_instance()
		# Attribute---------------------------
		self.font_metrics = QtGui.QFontMetrics(QtWidgets.QLabel().font())
		# Setting---------------------------
		self.setObjectName("AutoSuffixPopUpWindowID")
		self.setWindowTitle(f"auto suffix options")
		self.setWindowFlags(QtCore.Qt.Popup)
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layout()
		self.create_connections()
	
	def create_widgets(self):
		self.scroll_area   = QtWidgets.QScrollArea()
		self.scroll_widget = QtWidgets.QWidget()
		self.scroll_area.setStyleSheet(self.scroll_style)
		
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
		self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.scroll_area.setWidget(self.scroll_widget)
	
	def create_layout(self):
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		
		self.main_layout.addWidget(self.scroll_area)

		self.scroll_widget_layout = QtWidgets.QFormLayout(self.scroll_widget)
		self.scroll_widget_layout.setContentsMargins(5, 0, 0, 0)
		self.scroll_widget_layout.setSpacing(0)
		
		
	def create_connections(self):
		pass
	
	def add_content_selected_type(self, type_list = [ ], icon_list = [ ], size_list = [ ]):
		self.clear_form_layout(self.scroll_widget_layout)
		
		if type_list:
			for index, obj in enumerate(type_list):
				grp_layout = QtWidgets.QHBoxLayout()
				icon       = CustomLabelIconPopUP(icon_list[index], size_list[index])
				editline   = CustomQLineEditAutoSuffixPopUP(type_list[index])
				
				grp_layout.addWidget(icon)
				grp_layout.addWidget(editline)
				
				self.scroll_widget_layout.addRow(f"{type_list[index]}: ", grp_layout)
		
		text_width = self.get_text_width(type_list)
		self.set_resize_popup(text_width, len(type_list))
		
		
	def get_text_width(self, list_name = [ ]):
		if list_name:
			longest_name = max(list_name, key=len)
			text_width   = self.font_metrics.horizontalAdvance(longest_name)
		else:
			text_width   = 0
		
		return text_width
	
	def set_resize_popup(self, width, count):
		if count > 10:
			Y = 250
			X = width + 25 + 60 + 20
		elif count == 0:
			Y = 25
			X = 50
		else:
			Y = count*25
			X = width + 25 + 60 + 15
			
		self.setFixedSize(X,Y)
		self.resize(X,Y)
		
	def clear_form_layout(self, layout):
		while layout.count():
			item = layout.takeAt(0)
			if item.widget():
				item.widget().deleteLater()
			elif item.layout():
				self.clear_form_layout(item.layout())
				item.layout().deleteLater()
	

class CustomQLineEditAutoSuffixPopUP(QtWidgets.QLineEdit):
	"""
	Class for creating a customizable input field.
	"""
	
	Style_lineEdit = """
		    QLineEdit {
		        background-color: rgb(40, 40, 40);  /* Темно-серый фон */
		        border: 2px solid rgb(100, 100, 100);  /* Серо-черная граница */
		        border-radius: 10px;
		        padding: 0 4px;
		        color: rgb(220, 220, 220);          /* Светло-серый текст */
		        selection-background-color: rgb(88, 88, 120); /* Темно-серый фон для выделения */
		        selection-color: rgb(255, 255, 255);  /* Белый текст при выделении */
		    }

		    QLineEdit:hover {
		        border: 2px solid rgb(100, 100, 100);  /* Светло-серая граница при наведении */
		        background-color: rgb(45, 45, 45);     /* Немного светлее при наведении */
		    }

		    QLineEdit:focus {
		        color: rgb(255, 255, 255);           /* Белый текст при фокусе */
		        border: 2px solid rgb(120, 120, 120); /* Ярче серый при фокусе */
		        background-color: rgb(50, 50, 50);    /* Более светлый серый при фокусе */
		    }

		    QLineEdit:hover:focus {
		        border: 2px solid rgb(150, 150, 150); /* Светлая граница при наведении и фокусе */
		        background-color: rgb(55, 55, 55);    /* Еще более светлый фон при наведении и фокусе */
		    }
		"""
	
	def __init__(self, type_obj, parent=None):
		super(CustomQLineEditAutoSuffixPopUP, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.type_obj = type_obj
		self.suffix = self.resources.config.get_variable("auto_suffix", self.type_obj, "", str)
		self.toolTip = f"{self.suffix} The auto suffix is for [{self.type_obj}]"
		# Setting---------------------------
		self.setText(self.suffix)
		self.setFixedSize(60, 25)
		self.setStyleSheet(self.Style_lineEdit)
		self.setToolTip(self.toolTip)
		self.setAlignment(QtCore.Qt.AlignHCenter)
		self.setPlaceholderText("suffix")
		# Run functions ---------------------------
		self.create_connections()
	
	def create_connections(self):
		self.textEdited.connect(self.set_suffix)
	
	def set_suffix(self, suffix):
		if suffix != self.suffix:
			self.suffix = suffix
			self.toolTip = f"{self.suffix} The auto suffix is for [{self.type_obj}]"
			self.setToolTip(self.toolTip)
			self.resources.config.set_variable("auto_suffix", self.type_obj, suffix)
	
	def contextMenuEvent(self, event):
		pass


class CustomLabelIconPopUP(QtWidgets.QLabel):
	"""
	Display show the icon of the object type.
	"""

	def __init__(self, icon, size, parent=None):
		super(CustomLabelIconPopUP, self).__init__(parent)
		
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon = icon
		self.size = size
		pixmap    = self.icon.pixmap(self.size, self.size)
		# Setting---------------------------
		self.setPixmap(pixmap)
		self.setFixedSize(self.size, self.size)
		# Run functions ---------------------------
		self.create_connections()
	
	def create_connections(self):
		pass