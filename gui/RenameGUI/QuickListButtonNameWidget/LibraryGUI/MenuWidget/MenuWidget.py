try:
	from PySide2 import QtWidgets, QtGui, QtCore
	from PySide2.QtWidgets import QAction
	from PySide2.QtGui import QGraphicsOpacityEffect
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	from PySide6.QtGui import QAction
	from PySide6.QtWidgets import QGraphicsOpacityEffect

from MSL_MayaRename.core.resources import Resources

class MenuWidget(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(MenuWidget, self).__init__(parent)
		# Modul---------------------------
		# Attribute---------------------------
		# Setting---------------------------
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.setFixedHeight(25)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	def create_widgets(self):
		self.save_btn = SaveQPushButton()
		self.reset_btn = ResetQPushButton()
		self.duplicate_btn = DuplicateQPushButton()
	
	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
		
		self.main_layout.addWidget(self.save_btn)
		self.main_layout.addWidget(self.reset_btn)
		self.main_layout.addWidget(self.duplicate_btn)
		
	
	def create_connections(self):
		pass
		
		
class SaveQPushButton(QtWidgets.QPushButton):
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
	itSave = QtCore.Signal()
	
	def __init__(self, parent = None):
		super(SaveQPushButton, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon_save = self.resources.get_icon_from_resources("save-svgrepo-com_v1.svg")
		self._tooltip  = "Save library"
		self.opacity_effect = QGraphicsOpacityEffect(self)
		# Setting---------------------------
		self.setIcon(self.icon_save)
		self.setIconSize(QtCore.QSize(18, 18))
		self.setFixedSize(25, 25)
		self.setStyleSheet(self.Style_btn)
		self.setToolTip(self._tooltip)
		self.setEnabled(False)
		self.setGraphicsEffect(self.opacity_effect)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_connections()
	
	def create_widgets(self):
		self.animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
		self.animation.setDuration(300)
	
	def create_connections(self):
		self.clicked.connect(self.on_click_save)
	
	def on_click_save(self):
		self.itSave.emit()
		
	def set_Enabled(self, bool):
		if self.isEnabled() != bool:
			start_opacity = 0.5 if bool else 1.0
			end_opacity =  1.0 if bool else 0.5
			
			self.animation.stop()
			self.animation.setStartValue(start_opacity)
			self.animation.setEndValue(end_opacity)
			self.animation.start()
			
			self.setEnabled(bool)
	
	def enterEvent(self, event):
		super(SaveQPushButton, self).enterEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)
	
	def leaveEvent(self, event):
		super(SaveQPushButton, self).leaveEvent(event)
		self.setCursor(QtCore.Qt.ArrowCursor)
	
	def mouseReleaseEvent(self, event):
		super(SaveQPushButton, self).mouseReleaseEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)
	
	def mousePressEvent(self, event):
		super(SaveQPushButton, self).mousePressEvent(event)

		
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
		self.resources  = Resources.get_instance()
		# Attribute---------------------------
		self.icon_reset = self.resources.get_icon_from_resources("power-button-svgrepo-com.svg")
		self._tooltip   = "Reset library"
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
		self.clicked.connect(self.on_click_reset)
	
	def on_click_reset(self):
		self.itReset.emit()
		
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


class DuplicateQPushButton(QtWidgets.QPushButton):
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
	itDuplicate = QtCore.Signal()
	
	def __init__(self, parent=None):
		super(DuplicateQPushButton, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon_reset = self.resources.get_icon_from_resources("clipboard-copy-duplicate-report-business-office-svgrepo-com")
		self._tooltip = "Duplicate of a name in library"
		# Setting---------------------------
		self.setIcon(self.icon_reset)
		self.setIconSize(QtCore.QSize(20, 20))
		self.setFixedSize(25, 25)
		self.setStyleSheet(self.Style_btn)
		self.setToolTip(self._tooltip)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_connections()
	
	def create_widgets(self):
		pass
	
	def create_connections(self):
		self.clicked.connect(self.on_click_reset)
	
	def on_click_reset(self):
		self.itDuplicate.emit()
	
	def enterEvent(self, event):
		super(DuplicateQPushButton, self).enterEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)
	
	def leaveEvent(self, event):
		super(DuplicateQPushButton, self).leaveEvent(event)
		self.setCursor(QtCore.Qt.ArrowCursor)
	
	def mouseReleaseEvent(self, event):
		super(DuplicateQPushButton, self).mouseReleaseEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)
	
	def mousePressEvent(self, event):
		super(DuplicateQPushButton, self).mousePressEvent(event)
