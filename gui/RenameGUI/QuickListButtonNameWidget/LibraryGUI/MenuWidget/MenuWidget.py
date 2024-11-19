try:
	from PySide2 import QtWidgets, QtGui, QtCore
	from PySide2.QtWidgets import QAction
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	from PySide6.QtGui import QAction

from MSL_MayaRename.core.resources import Resources

class MenuWidget(QtWidgets.QWidget):
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

		    """
	Style_btn_reset = """
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
	def __init__(self, parent=None):
		super(MenuWidget, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.icon_save         = self.resources.get_icon_from_resources("diskette-save-svgrepo-com.svg")
		self.icon_reset        = self.resources.get_icon_from_resources("power-button-svgrepo-com.svg")
		self.icon_duplicate    = self.resources.get_icon_from_resources("clipboard-copy-duplicate-report-business-office-svgrepo-com.svg")
		# Setting---------------------------
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.setFixedHeight(25)
		

		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	def create_widgets(self):
		self.save_btn = QtWidgets.QPushButton()
		self.save_btn.setIcon(self.icon_save)
		self.save_btn.setIconSize(QtCore.QSize(20, 20))
		self.save_btn.setFixedSize(25, 25)
		self.save_btn.setStyleSheet(self.Style_btn)
		self.save_btn.setToolTip("Save")
		self.save_btn.setCheckable(True)
		self.save_btn.setChecked(True)
		self.save_btn.setEnabled(False)
		
		self.reset_btn = QtWidgets.QPushButton()
		self.reset_btn.setFixedSize(25, 25)
		self.reset_btn.setIcon(self.icon_reset)
		self.reset_btn.setIconSize(QtCore.QSize(20, 20))
		self.reset_btn.setStyleSheet(self.Style_btn_reset)
		self.reset_btn.setToolTip("reset")
		
		self.duplicate_btn = QtWidgets.QPushButton()
		self.duplicate_btn.setFixedSize(25, 25)
		self.duplicate_btn.setIcon(self.icon_duplicate)
		self.duplicate_btn.setIconSize(QtCore.QSize(20, 20))
		self.duplicate_btn.setStyleSheet(self.Style_btn_reset)
		self.duplicate_btn.setToolTip("duplicate")
	
	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
		
		self.main_layout.addWidget(self.reset_btn)
		self.main_layout.addWidget(self.duplicate_btn)
		self.main_layout.addWidget(self.save_btn)
	
	def create_connections(self):
		pass
		