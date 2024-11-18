try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core import icon_rc
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.CustumeLineEditorWidget import CustumeLineEditorWidget


class addCategoryWidget(QtWidgets.QWidget):
	
	isCategoryName = QtCore.Signal(str)
	
	Style_comboBox = """
		QComboBox {
		    background-color: rgb(40, 40, 40);
		    border: 2px solid rgb(80, 80, 80);
		    border-radius: 6px;
		    padding: 4px;
		    color: rgb(220, 220, 220);
		}
		
		QComboBox:hover {
		    border: 2px solid rgb(100, 100, 100);
		    background-color: rgb(45, 45, 45);
		}
		

		
		QComboBox::drop-down {
		    background-color: rgb(40, 40, 40);
		    border: 1px solid rgb(80, 80, 80);
		    border-top-right-radius: 4px; /* Радиус правой верхней части */
            border-bottom-right-radius: 4px; /* Радиус правой нижней части */
		    width: 20px;
		}
		
		QComboBox::down-arrow {
		    image: url(":/icon/crab-svgrepo-com.svg");
		    width: 25px;
		    height: 25px;
		    background: none;
		}
		
		QComboBox QAbstractItemView {
		    background-color: rgb(40, 40, 40);
		    selection-background-color: rgb(88, 88, 120);
		    selection-color: rgb(255, 255, 255);
		    border: 2px solid rgb(70, 70, 70);
		    border-radius: 6px;
		}
	"""
	
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
	
	def __init__(self, state, parent=None):
		super(addCategoryWidget, self).__init__(parent)
		
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.tooltip = f"Addition of a category name"
		self.state   = state
		# Setting---------------------------
		self.setFixedHeight(25)
		self.setVisible(self.state)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	def create_widgets(self):
		self.add_lineEdit = CustumeLineEditorWidget("Category", 80, 25)
		self.add_button   = QPushButtonAddName("+")
	
	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignHCenter)
		
		self.main_layout.addWidget(self.add_lineEdit)
		self.main_layout.addWidget(self.add_button)
	
	def create_connections(self):
		self.add_button.clicked.connect(self.on_clicked)
		self.add_lineEdit.returnPressed.connect(self.on_clicked)
	
	def on_clicked(self):
		name = self.add_lineEdit.text()
		self.isCategoryName.emit(name)


class QPushButtonAddName(QtWidgets.QPushButton):
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
	
	def __init__(self, name, parent=None):
		super(QPushButtonAddName, self).__init__(name, parent)
		
		self.setFixedSize(25, 25)
		self.setStyleSheet(self.Style_btn)
	
	def enterEvent(self, event):
		super(QPushButtonAddName, self).enterEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)
	
	def leaveEvent(self, event):
		super(QPushButtonAddName, self).leaveEvent(event)
		self.setStyleSheet(self.Style_btn)
		self.setCursor(QtCore.Qt.ArrowCursor)
	
	def mouseReleaseEvent(self, event):
		super(QPushButtonAddName, self).mouseReleaseEvent(event)
		self.setCursor(QtCore.Qt.PointingHandCursor)
	
	def mousePressEvent(self, event):
		super(QPushButtonAddName, self).mousePressEvent(event)
	