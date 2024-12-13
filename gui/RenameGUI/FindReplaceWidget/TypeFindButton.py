try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources


class TypeFindButton(QtWidgets.QPushButton):
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
	TYPE_LIST = ["selected", "hierarchy", "all"]
	
	
	def __init__(self, parent=None):
		super(TypeFindButton, self).__init__(parent)
		# Module---------------------------
		self.resoures = Resources.get_instance()
		# Attribute---------------------------
		self.type = self.resoures.config.get_variable("startup", "type_find", "selected", str)
		self.current_index = 0
		# Setting---------------------------
		self.setFixedSize(25, 25)
		self.setToolTip(self.type)
		self.setStyleSheet(self.Style_btn)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
	
		# Run functions ---------------------------
		self.create_widgets()
		self.create_connections()
		self.set_name_btn(self.type)
		
	def create_widgets(self):
		self.pop_up_window = PopUpWindow(self)
		
		
	def create_connections(self):
		self.clicked.connect(self.update_name)
		self.customContextMenuRequested.connect(self.show_pop_up_window)
		self.pop_up_window.btn_grp.buttonClicked.connect(self.on_button_clicked)
	
	def show_pop_up_window(self, pos):
		"""
		Displays the pop-up window at the position of the button.
		"""
		pop_up_pos = self.mapToGlobal(QtCore.QPoint(0, 25))

		self.pop_up_window.move(pop_up_pos)
		self.pop_up_window.show()
	
	def on_button_clicked(self, btn):
		type = btn.text()
		self.set_name_btn(type)
	
	def update_name(self):
		self.current_index = (self.current_index + 1) % len(self.TYPE_LIST)
		type = self.TYPE_LIST[self.current_index]
		self.pop_up_window.set_checked_btn(type)
		self.set_name_btn(type)
	
	def set_name_btn(self, type):
		self.type = type
		
		if type == "selected":
			name = "sel"
			self.current_index = 0
		elif type == "hierarchy":
			name = "hi"
			self.current_index = 1
		elif type == "all":
			name = "all"
			self.current_index = 2
			
		self.setText(name)
		self.setToolTip(self.type)
		self.resoures.config.set_variable("startup", "type_find", self.type)
	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(TypeFindButton, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		self.setStyleSheet(self.Style_btn)
		super(TypeFindButton, self).leaveEvent(event)


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
		self.hi  = QtWidgets.QRadioButton("hierarchy")
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

