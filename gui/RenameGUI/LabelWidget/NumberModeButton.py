try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources


class NumberModeButton(QtWidgets.QPushButton):

	changeStateNumberMode = QtCore.Signal(bool)
	itPrefixNumber = QtCore.Signal(str)
	itSuffixNumber = QtCore.Signal(str)
	Style_btn = """
	        QPushButton {
	            background-color: rgb(50, 50, 50); /* Темно-серый фон */
	            border-style: outset;
	            border-width: 2px;
	            border-radius: 8px;
	            border-color: rgb(30, 30, 30); /* Темнее границы */
	            font: bold 14px; /* Жирный шрифт */
	            font-family: Arial; /* Шрифт Arial */
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

	        QPushButton:checked {
	            background-color: rgb(80, 120, 80); /* Зеленоватый оттенок при нажатии (состояние check) */
	            border-color: rgb(60, 90, 60); /* Темно-зеленая граница при нажатии */
	            color: rgb(240, 240, 240); /* Белый текст */
	        }

	        QPushButton:checked:hover {
	            background-color: rgb(100, 140, 100); /* Светлее при наведении в состоянии checked */
	            border-color: rgb(80, 110, 80); /* Светлее при наведении в состоянии checked */
	        }
	    """

	def __init__(self, name="", width=25,height=25,icon="", parent=None):
		super(NumberModeButton, self).__init__(parent)

		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self._width     = width
		self._height    = height
		self.tooltip   = f"Numeric Mode: Adds Numbers to Words"
		self.icon      = self.resources.get_icon_from_resources(icon if icon else "cooperate-svgrepo-com.svg")
		self.has_state = self.resources.config.get_variable("startup", "mode_number", False, bool)
		# Setting---------------------------
		self.setText(name)
		self.setFixedSize(self._width,self._height)
		self.setToolTip(self.tooltip)
		self.setStyleSheet(self.Style_btn)
		self.setIcon(self.icon)
		self.setCheckable(True)
		self.setChecked(self.has_state)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_connections()

	def create_widgets(self):
		self.pop_up_window = PopUpWindow(self)

	def create_connections(self):
		self.clicked.connect(self.is_active_mode)
		self.customContextMenuRequested.connect(self.show_pop_up_window)
		self.pop_up_window.prefix_num.itPrefixNumber.connect(lambda prefix: self.itPrefixNumber.emit(prefix))
		self.pop_up_window.suffix_num.itSuffixNumber.connect(lambda suffix: self.itSuffixNumber.emit(suffix))
		
	def show_pop_up_window(self, pos):
		"""
		Displays the pop-up window at the position of the button.
		"""
		pop_up_pos = self.mapToGlobal(QtCore.QPoint(self._width, 0))

		self.pop_up_window.move(pop_up_pos)
		self.pop_up_window.prefix_num.clearFocus()
		self.pop_up_window.suffix_num.clearFocus()
		self.pop_up_window.show()

	def is_active_mode(self, Checkable):
		self.resources.config.set_variable("startup", "mode_number", Checkable)
		self.changeStateNumberMode.emit(Checkable)
	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(NumberModeButton, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		self.setStyleSheet(self.Style_btn)
		super(NumberModeButton, self).leaveEvent(event)
		
class PopUpWindow(QtWidgets.QWidget):
	"""
	Class for creating a pop-up window with options.
	"""

	def __init__(self, parent=None):
		super(PopUpWindow, self).__init__(parent)

		# Attribute---------------------------
		# Setting---------------------------
		self.setWindowTitle(f"Number mode Options")
		self.setWindowFlags(QtCore.Qt.Popup)
		self.setFixedSize(96, 79)

		# Run functions ---------------------------
		self.create_widgets()
		self.create_layout()

	def create_widgets(self):
		self.prefix_num  = CustomQLineEditPrefixNumberPopUP()
		self.suffix_num  = CustomQLineEditSuffixNumberPopUP()
		self.letter_mode = CustomPushButtonModeLetterPopUP()


	def create_layout(self):
		# main layout---------------------------
		self.main_layout = QtWidgets.QFormLayout(self)
		self.main_layout.setContentsMargins(5, 2, 5, 2)
		self.main_layout.setSpacing(0)
		# add widget----------------------------
		self.main_layout.addRow("Prefix: ", self.prefix_num)
		self.main_layout.addRow("Suffix: ", self.suffix_num)
		self.main_layout.addRow("Letter: ", self.letter_mode)


	def create_connections(self):
		pass

class CustomQLineEditPrefixNumberPopUP(QtWidgets.QLineEdit):
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
	itPrefixNumber = QtCore.Signal(str)
	def __init__(self, width = 50, height = 25, parent=None):
		super(CustomQLineEditPrefixNumberPopUP, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.prefix  = self.resources.config.get_variable("startup", "prefix_number", "", str)
		self._width  = width
		self._height = height
		self.toolTip = f"Prefix of the number [{self.prefix}]"
		# Setting---------------------------
		self.setText(self.prefix)
		self.setFixedSize(self._width, self._height)
		self.setStyleSheet(self.Style_lineEdit)
		self.setToolTip(self.toolTip)
		self.setAlignment(QtCore.Qt.AlignHCenter)
		self.setPlaceholderText("prefix")
		# Run functions ---------------------------
		self.create_connections()

	def create_connections(self):
		self.textEdited.connect(self.set_prefix)

	def set_prefix(self, prefix):
		if prefix != self.prefix:
			self.prefix  = prefix
			self.toolTip = f"Prefix of the number [ {self.prefix} ]"
			self.setToolTip(self.toolTip)
			self.resources.config.set_variable("startup", "prefix_number", prefix)
			self.itPrefixNumber.emit(prefix)

	def contextMenuEvent(self, event):
		pass
	
class CustomQLineEditSuffixNumberPopUP(QtWidgets.QLineEdit):
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
	itSuffixNumber = QtCore.Signal(str)

	def __init__(self, width = 50, height = 25, parent=None):
		super(CustomQLineEditSuffixNumberPopUP, self).__init__(parent)
		
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.suffix  = self.resources.config.get_variable("startup", "suffix_number", "", str)
		self._width  = width
		self._height = height
		self.toolTip = f"Suffix of the number [ {self.suffix} ]"
		
		# Setting---------------------------
		self.setText(self.suffix)
		self.setFixedSize(self._width, self._height)
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
			self.suffix  = suffix
			self.toolTip = f"Suffix of the number [ {self.suffix} ]"
			self.setToolTip(self.toolTip)
			self.resources.config.set_variable("startup", "suffix_number", suffix)
			self.itSuffixNumber.emit(suffix)

	def contextMenuEvent(self, event):
		pass


class CustomPushButtonModeLetterPopUP(QtWidgets.QPushButton):
	"""
	Display show the Letter Mode.
	"""
	
	Style_btn = """
		        QPushButton {
		            background-color: rgb(50, 50, 50); /* Темно-серый фон */
		            border-style: outset;
		            border-width: 2px;
		            border-radius: 8px;
		            border-color: rgb(30, 30, 30); /* Темнее границы */
		            font: bold 14px; /* Жирный шрифт */
		            font-family: Arial; /* Шрифт Arial */
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

		        QPushButton:checked {
		            background-color: rgb(80, 120, 80); /* Зеленоватый оттенок при нажатии (состояние check) */
		            border-color: rgb(60, 90, 60); /* Темно-зеленая граница при нажатии */
		            color: rgb(240, 240, 240); /* Белый текст */
		        }

		        QPushButton:checked:hover {
		            background-color: rgb(100, 140, 100); /* Светлее при наведении в состоянии checked */
		            border-color: rgb(80, 110, 80); /* Светлее при наведении в состоянии checked */
		        }
		    """
	itShowLetter = QtCore.Signal(bool)
	
	def __init__(self, parent=None):
		super(CustomPushButtonModeLetterPopUP, self).__init__(parent)
		
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon = self.resources.get_icon_from_resources("letter-spacing-01-svgrepo-com.svg")
		self.has_state = self.resources.config.get_variable("startup", "mode_letter", False, bool)
		self.toolTip = f"Show the Letter mode"
		# Setting---------------------------
		self.setFixedSize(25, 25)
		self.setStyleSheet(self.Style_btn)
		self.setToolTip(self.toolTip)
		self.setIcon(self.icon)
		self.setCheckable(True)
		self.setChecked(self.has_state)
		
		self.create_connections()
	
	def create_connections(self):
		self.clicked.connect(self.on_show_cache)
	
	def on_show_cache(self, state):
		self.resources.config.set_variable("startup", "mode_letter", state)
		self.has_state = state
		self.setChecked(self.has_state)
		
		self.itShowLetter.emit(state)
	
	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(CustomPushButtonModeLetterPopUP, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(CustomPushButtonModeLetterPopUP, self).leaveEvent(event)
