from sys import prefix

try:
	from PySide2 import QtWidgets, QtGui, QtCore
	from shiboken2 import wrapInstance
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	from shiboken6 import wrapInstance

from xml.etree.ElementTree import Element, SubElement, tostring
from functools import partial
from MSL_MayaRename.core.resources import Resources
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui
import sys


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
		self.toolTip           = "Automatic prefix addition."
		self.script_job_number = -1
		self.combination       = None
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
		
		self.pop_up_window = PopUpWindow(self)
	
	def create_layouts(self):
		self.Colorlayout = QtWidgets.QHBoxLayout(self)
		self.Colorlayout.setContentsMargins(0, 0, 0, 0)
		self.Colorlayout.setSpacing(0)
		
		self.Colorlayout.addWidget(self.rt_widget)
		self.Colorlayout.addWidget(self.mid_widget)
		self.Colorlayout.addWidget(self.lf_widget)
		
		
	
	def create_connections(self):
		self.customContextMenuRequested.connect(self.show_pop_up_window)
		self.pop_up_window.change_color.connect(lambda : self.update_icon(self.combination))
		self.clicked.connect(self.set_auto_prefix)
		self.pop_up_window.itChangeMirror.connect(self.update_selection)
	
	def check_prefix(self, name):
		
		lf = self.resources.config.get_variable("auto_prefix", "left", "", str)
		rt = self.resources.config.get_variable("auto_prefix", "right", "", str)
		mid = self.resources.config.get_variable("auto_prefix", "center", "", str)
		
		prefixes = tuple(prefix for prefix in (lf, rt, mid) if prefix) + ("lf_", "rt_", "mid_")
		
		if name.startswith(prefixes):
			parts = name.split("_")
			name = "_".join(parts[1:])
			
		return name
	
	def set_auto_prefix(self):
		selection = cmds.ls(selection=True, l=True)
		if selection:
			filtered_list = self.parent().parent().FindReplaceWidget.remove_shapes_from_transforms(selection)
			
			for obj in filtered_list:
				type_obj = cmds.objectType(obj)
				if type_obj == "transform" or type_obj == "joint":
					position = self.classify_object_position(obj)
					if position == "lf":
						prefix = self.resources.config.get_variable("auto_prefix", "left", "", str)
					elif position == "rt":
						prefix = self.resources.config.get_variable("auto_prefix", "right", "", str)
					elif position == "mid":
						prefix = self.resources.config.get_variable("auto_prefix", "center", "", str)
				else:
					continue

				if not prefix:
					continue
				
				path_to_obj, obj_short_name = self.parent().parent().get_short_name(obj)
				
				if obj_short_name[:len(prefix)] == prefix:
					continue
					
				obj_short_name = self.check_prefix(obj_short_name)
				# print(f"{type_obj:<10}: {position:<5}: {obj_short_name:<20}: {prefix}")
				
				new_obj_short_name = prefix + obj_short_name
				obj_rename = cmds.rename(obj, new_obj_short_name)
				
				new_path_to_obj, new_obj_short_name = self.parent().parent().get_short_name(obj_rename)
				new_obj = path_to_obj + new_obj_short_name
				
				filtered_list = self.parent().parent().renameObjectsInHierarchy(filtered_list, obj, new_obj)
			
			self.parent().parent().LabelWidget.update_selection()
		
		else:
			print("It is necessary to select an object.")
		
		
	
	def update_selection(self):
		"""
		Updates the current selection of objects in the scene and reflects this in the UI.
		"""
		self.combination = [ ]
		selection = cmds.ls(selection=True, l=True)
		
		if selection:
			for obj in selection:
				type_obj = cmds.objectType(obj)
				if type_obj == "transform" or type_obj == "joint":
					position = self.classify_object_position(obj)
					if position not in self.combination:
						self.combination.append(position)
		
		self.update_icon(combination = self.combination)


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
			size = 20
		else:
			icon = self.icon
			size = 25

			
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(size, size))
	
	def classify_object_position(self, obj_name):
		"""
		Determines the position of an object relative to a given mirror axis.
		"""
		try:
			position = cmds.xform(obj_name, q=True, t=True, ws=True)
		except Exception as e:
			raise RuntimeError(f"Failed to get object position '{obj_name}': {e}")
		
		mirror_across = self.resources.config.get_variable("auto_prefix", "mirror_across", "YZ", str)
		axis_mapping = {"YZ": 0,"XZ": 1, "XY": 2}
		
		if mirror_across not in axis_mapping:
			raise ValueError(f"Invalid value 'mirror_across': {mirror_across}")
		
		axis_index = axis_mapping[mirror_across]
		pos_value = position[axis_index]
		
		if pos_value < 0:
			return "rt"
		elif pos_value == 0:
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

		pop_up_pos = self.mapToGlobal(QtCore.QPoint(0, 25))
		self.pop_up_window.update_color_btn()
		self.pop_up_window.move(pop_up_pos)
		self.pop_up_window.show()

	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(AutoPrefixButton, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		self.setStyleSheet(self.Style_btn)
		super(AutoPrefixButton, self).leaveEvent(event)


class PopUpWindow(QtWidgets.QWidget):
	"""
	Class for creating a pop-up window with options.
	"""
	Style_comboBox = """
		    QComboBox {
		        background-color: rgb(40, 40, 40);
		        border: 2px solid rgb(80, 80, 80);
		        border-radius: 6px;
		        padding: 4px;
		        color: rgb(255, 204, 153);
		    }

		    QComboBox:hover {
		        border: 2px solid rgb(100, 100, 100);
		        background-color: rgb(45, 45, 45);
		    }

		    QComboBox::drop-down {
		        width: 0; /* Убираем выпадающую область */
		    }

		    QComboBox::down-arrow {
		        width: 0; /* Убираем стрелочку */
		        height: 0;
		    }
			"""
	ColorDefault = {"lf": "#8FD14F", "rt": "#FF6F61", "mid": "#FFD25A" }
	change_color = QtCore.Signal()
	itChangeMirror = QtCore.Signal()
	
	def __init__(self, parent=None):
		super(PopUpWindow, self).__init__(parent)
		# Module---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.mirror_list   = ["YZ", "XY", "XZ"]
		self.currentMirror = self.resources.config.get_variable("auto_prefix", "mirror_across", "YZ", str)
		self.lf_color      = self.resources.config.get_variable("auto_prefix", "lf_color", "#FF6F61", str)  # #C0C0C0
		self.rt_color      = self.resources.config.get_variable("auto_prefix", "rt_color", "#8FD14F", str)  # #CD7F32
		self.mid_color     = self.resources.config.get_variable("auto_prefix", "mid_color", "#FFD25A", str)  # #FFD700
		self.icon_path     = self.resources.icon_path + "/"
		# Setting---------------------------
		self.setWindowTitle(f"Number mode Options")
		self.setWindowFlags(QtCore.Qt.Popup)
		self.setFixedSize(150, 100)
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layout()
		self.create_connections()
	
	def create_widgets(self):
		self.prefix_lf  = CustomQLineEditPrefixPopUP("left")
		self.prefix_rt  = CustomQLineEditPrefixPopUP("right")
		self.prefix_mid = CustomQLineEditPrefixPopUP("center")
		
		self.color_lf_btn   = CustomColorButton(self.lf_color)
		self.color_rt_btn   = CustomColorButton(self.rt_color)
		self.color_mid_btn  = CustomColorButton(self.mid_color)
		
		self.reset_btn = ResetQPushButton()

		self.combobox = QtWidgets.QComboBox()
		self.combobox.setFixedSize(25, 25)
		self.combobox.setStyleSheet(self.Style_comboBox)
		for i in self.mirror_list:
			self.combobox.addItem(i)
		self.combobox.setCurrentText(self.currentMirror)
		
	
	def create_layout(self):
		# main layout---------------------------
		self.main_layout = QtWidgets.QFormLayout(self)
		self.main_layout.setContentsMargins(5, 2, 5, 2)
		self.main_layout.setSpacing(0)
		
		self.layout_mirror = QtWidgets.QHBoxLayout()
		self.layout_mirror.addWidget(self.combobox)
		self.layout_mirror.addWidget(self.reset_btn)
		
		self.layout_lf = QtWidgets.QHBoxLayout()
		self.layout_lf.addWidget(self.prefix_lf)
		self.layout_lf.addWidget(self.color_lf_btn)
		
		self.layout_rt = QtWidgets.QHBoxLayout()
		self.layout_rt.addWidget(self.prefix_rt)
		self.layout_rt.addWidget(self.color_rt_btn)
		
		self.layout_mid = QtWidgets.QHBoxLayout()
		self.layout_mid.addWidget(self.prefix_mid)
		self.layout_mid.addWidget(self.color_mid_btn)
		
		
		# add widget----------------------------
		self.main_layout.addRow("Mirror across: ", self.layout_mirror)
		self.main_layout.addRow("Right side: ", self.layout_rt)
		self.main_layout.addRow("Сenter side: ", self.layout_mid)
		self.main_layout.addRow("Left side: ", self.layout_lf)

	
	def create_connections(self):
		self.combobox.currentTextChanged.connect(self.update_current_mirror)
		self.color_lf_btn.color_changed.connect(lambda color: self.set_color_icon(color, "lf"))
		self.color_rt_btn.color_changed.connect(lambda color: self.set_color_icon(color, "rt"))
		self.color_mid_btn.color_changed.connect(lambda color: self.set_color_icon(color, "mid"))
		self.reset_btn.clicked.connect(self.on_reset)
	
	def on_reset(self):
		self.set_color_icon(QtGui.QColor(self.ColorDefault["lf"]), "lf")
		self.set_color_icon(QtGui.QColor(self.ColorDefault["rt"]), "rt")
		self.set_color_icon(QtGui.QColor(self.ColorDefault["mid"]), "mid")
		self.update_color_btn()
		self.combobox.setCurrentText("YZ")
		self.prefix_lf.set_prefix("lf_")
		self.prefix_lf.setText("lf_")
		self.prefix_rt.set_prefix("rt_")
		self.prefix_rt.setText("rt_")
		self.prefix_mid.set_prefix("")
		self.prefix_mid.setText("")
	
	def set_color_icon(self, color, side):
		color = color.name()
		if side == "lf":
			if self.lf_color != color:
				self.lf_color = color
				self.resources.config.set_variable("auto_prefix", "lf_color", color)
		elif side == "rt":
			if self.rt_color != color:
				self.resources.config.set_variable("auto_prefix", "rt_color", color)
				self.rt_color = color
		elif side == "mid":
			if self.mid_color != color:
				self.resources.config.set_variable("auto_prefix", "mid_color", color)
				self.mid_color = color
				
		self.run_create_svg()
		self.change_color.emit()
		
		
	def update_color_btn(self):
		for i in range(self.layout_lf.count()):
			item = self.layout_lf.itemAt(i)
			widget = item.widget()
			if isinstance(widget, CustomColorButton):

				self.layout_lf.takeAt(i)
				widget.deleteLater()
				self.color_lf_btn = CustomColorButton(self.lf_color)
				self.layout_lf.insertWidget(i, self.color_lf_btn)
				self.color_lf_btn.color_changed.connect(lambda color: self.set_color_icon(color, "lf"))
		
		for i in range(self.layout_rt.count()):
			item = self.layout_rt.itemAt(i)
			widget = item.widget()
			if isinstance(widget, CustomColorButton):

				self.layout_rt.takeAt(i)
				widget.deleteLater()
				self.color_rt_btn = CustomColorButton(self.rt_color)
				self.layout_rt.insertWidget(i, self.color_rt_btn)
				self.color_rt_btn.color_changed.connect(lambda color: self.set_color_icon(color, "rt"))
				
		for i in range(self.layout_mid.count()):
			item = self.layout_mid.itemAt(i)
			widget = item.widget()
			if isinstance(widget, CustomColorButton):

				self.layout_mid.takeAt(i)
				widget.deleteLater()
				self.color_mid_btn = CustomColorButton(self.mid_color)
				self.layout_mid.insertWidget(i, self.color_mid_btn)
				self.color_mid_btn.color_changed.connect(lambda color: self.set_color_icon(color, "mid"))

	def update_current_mirror(self, type):
		self.currentMirror = type
		self.resources.config.set_variable("auto_prefix", "mirror_across", type)
		self.itChangeMirror.emit()
	
	def run_create_svg(self):
		# Colors for the combinations
		# lf_color = "#FF6F61"  # #C0C0C0
		# mid_color = "#FFD25A"  # #FFD700
		# rt_color = "#8FD14F"  # #CD7F32
		
		combinations = [
			("lf.svg", "transparent", "transparent", self.lf_color),  # (lf)
			("lf_mid.svg", "transparent", self.mid_color, self.lf_color),  # (lf, mid)
			("lf_rf.svg", self.rt_color, "transparent", self.lf_color),  # (lf, rf)
			("lf_mid_rt.svg", self.rt_color, self.mid_color, self.lf_color),  # (lf, mid, rt)
			("rt.svg", self.rt_color, "transparent", "transparent"),  # (rt)
			("rt_mid.svg", self.rt_color, self.mid_color, "transparent"),  # (rt, mid)
			("mid.svg", "transparent", self.mid_color, "transparent")  # (mid)
		]

		# Create and save SVGs for all combinations
		for file_name, left, mid, right in combinations:
			self.create_svg_combination_circle(f"{self.icon_path}{file_name}", left, mid, right)
		
		# Returning paths to the created SVGs
		# print([self.icon_path + file_name for file_name, _, _, _ in combinations])
	
	
	def create_svg_combination_circle(self, file_name, left_color, mid_color, right_color):
		width = 25
		height = 25
		circle_radius = width // 6  # Радиус круга (1/6 ширины)
		circle_spacing = width // 3  # Расстояние между центрами кругов
		
		svg = Element('svg', xmlns="http://www.w3.org/2000/svg", width=str(width), height=str(height))
		
		# Левый круг
		SubElement(svg, 'circle', cx=str(circle_radius), cy=str(height // 2), r=str(circle_radius), fill=left_color)
		# Средний круг
		SubElement(svg, 'circle', cx=str(circle_spacing + circle_radius), cy=str(height // 2), r=str(circle_radius),
				   fill=mid_color)
		# Правый круг
		SubElement(svg, 'circle', cx=str(2 * circle_spacing + circle_radius), cy=str(height // 2), r=str(circle_radius),
				   fill=right_color)
		
		# Save the SVG to a file
		with open(file_name, "wb") as f:
			f.write(tostring(svg))

	def create_svg_combination(self, file_name, left_color, mid_color, right_color):
		width = 25
		height = 25
		bar_width = width // 3
		
		svg = Element('svg', xmlns="http://www.w3.org/2000/svg", width=str(width), height=str(height))
		SubElement(svg, 'rect', x="0", y="0", width=str(bar_width), height=str(height), fill=left_color)
		SubElement(svg, 'rect', x=str(bar_width), y="0", width=str(bar_width), height=str(height), fill=mid_color)
		SubElement(svg, 'rect', x=str(bar_width * 2), y="0", width=str(bar_width), height=str(height), fill=right_color)
		
		# Save the SVG to a file
		with open(file_name, "wb") as f:
			f.write(tostring(svg))


class CustomQLineEditPrefixPopUP(QtWidgets.QLineEdit):
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
	
	def __init__(self, side, parent=None):
		super(CustomQLineEditPrefixPopUP, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.side    = side
		self.prefix  = self.resources.config.get_variable("auto_prefix", self.side, "", str)
		self._width  = 50
		self._height = 25
		# Setting---------------------------
		self.setText(self.prefix)
		self.setFixedSize(self._width, self._height)
		self.setStyleSheet(self.Style_lineEdit)
		self.setAlignment(QtCore.Qt.AlignHCenter)
		self.setPlaceholderText(self.side)
		# Run functions ---------------------------
		self.create_connections()
	
	def create_connections(self):
		self.textEdited.connect(self.set_prefix)
	
	def set_prefix(self, prefix):
		if prefix != self.prefix:
			self.prefix = prefix
			self.resources.config.set_variable("auto_prefix", self.side, prefix)

	def contextMenuEvent(self, event):
		pass


class CustomColorButton(QtWidgets.QWidget):

	color_changed = QtCore.Signal(QtGui.QColor)

	def __init__(self, color=QtCore.Qt.white, parent=None):
		super(CustomColorButton, self).__init__(parent)
	
		self.setObjectName("CustomColorButton")
		self.create_control()
		self.set_size(14, 14)

		self.set_color(color)

	def create_control(self):
		""" 1) Create the colorSliderGrp """
		window = cmds.window()
		color_slider_name = cmds.colorSliderGrp()

		
		""" 2) Find the colorSliderGrp widget """
		self._color_slider_obj = omui.MQtUtil.findControl(color_slider_name)
		
		# Создание colorSliderGrp с текущим цветом
		current_color = self.get_color() if self._color_slider_obj else QtGui.QColor(QtCore.Qt.white)
		color_slider_name = cmds.colorSliderGrp(
			rgbValue=(current_color.redF(), current_color.greenF(), current_color.blueF()))
		
		if self._color_slider_obj:
			if sys.version_info.major >= 3:
				self._color_slider_widget = wrapInstance(int(self._color_slider_obj), QtWidgets.QWidget)
			else:
				self._color_slider_widget = wrapInstance(long(self._color_slider_obj), QtWidgets.QWidget)
				
			""" 3) Reparent the colorSliderGrp widget to this widget """
			main_layout = QtWidgets.QVBoxLayout(self)
			main_layout.setObjectName("main_layout")
			main_layout.setContentsMargins(0, 0, 0, 0)
			main_layout.addWidget(self._color_slider_widget)
			
			""" 4) Identify/store the colorSliderGrp�s child widgets (and hide if necessary)  """
			self._slider_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "slider")
			if self._slider_widget:
				self._slider_widget.hide()
				
			self._color_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "port")
			
			cmds.colorSliderGrp(self.get_full_name(), e=True, changeCommand=partial(self.on_color_changed))
			# Установка цвета в виджет
			self.set_color(current_color)
			
		cmds.deleteUI(window, window=True)

	def get_full_name(self):
		if sys.version_info.major >= 3:
			return omui.MQtUtil.fullName(int(self._color_slider_obj))
		else:
			return omui.MQtUtil.fullName(long(self._color_slider_obj))

	def set_size(self, width, height):
		self._color_slider_widget.setFixedWidth(width)
		self._color_widget.setFixedSize(width, height)

	def set_color(self, color):
		color = QtGui.QColor(color)
		if color != self.get_color():
			cmds.colorSliderGrp(self.get_full_name(), e=True, rgbValue=(color.redF(), color.greenF(), color.blueF()))
			self.on_color_changed()
	
	def get_color(self):
		color = cmds.colorSliderGrp(self.get_full_name(), q=True, rgbValue=True)
		color = QtGui.QColor(color[0] * 255, color[1] * 255, color[2] * 255)
		return color
		
	def on_color_changed(self, *args):
		self.color_changed.emit(self.get_color())


class ResetQPushButton(QtWidgets.QPushButton):
	Style_btn = """
		    QPushButton {
		        background-color: rgb(50, 50, 50); /* Темно-серый фон */
		        border-style: outset;
		        border-width: 2px;
		        border-radius: 6px;
		        border-color: rgb(30, 30, 30); /* Темнее границы */
		        font: bold 14px; /* Жирный шрифт */
		        font-family: Arial; /* Шрифт Arial */
		        color: rgb(200, 200, 200); /* Светло-серый текст */
		        padding: 5px; /* Внутренние отступы */
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
	itReset = QtCore.Signal()
	
	def __init__(self, parent=None):
		super(ResetQPushButton, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon_reset = self.resources.get_icon_from_resources("power-button-svgrepo-com.svg")
		self._tooltip = "Reset to dafault, color, position, name"
		# Setting---------------------------
		self.setIcon(self.icon_reset)
		self.setIconSize(QtCore.QSize(15, 15))
		self.setFixedSize(25, 25)
		self.setStyleSheet(self.Style_btn)
		self.setToolTip(self._tooltip)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_connections()
	
	def create_widgets(self):
		pass
	
	def create_connections(self):
		pass
	
	def enterEvent(self, event):
		super(ResetQPushButton, self).enterEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)
	
	def leaveEvent(self, event):
		super(ResetQPushButton, self).leaveEvent(event)
		self.setCursor(QtCore.Qt.ArrowCursor)
	
	def mouseReleaseEvent(self, event):
		super(ResetQPushButton, self).mouseReleaseEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)
	
	def mousePressEvent(self, event):
		super(ResetQPushButton, self).mousePressEvent(event)