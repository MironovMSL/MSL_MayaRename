try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core import icon_rc
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.CustumeLineEditorWidget import CustumeLineEditorWidget

class addSubCategoryWidget(QtWidgets.QWidget):
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
	
	def __init__(self, name="", width=100, height=25, icon="", parent=None):
		super(addSubCategoryWidget, self).__init__(parent)
		
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.width = width
		self.height = height
		self.tooltip = f"Addition of a subcategory name"
		# Setting---------------------------
		self.setFixedHeight(25)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
	
	def create_widgets(self):
		self.btn = QtWidgets.QComboBox()
		self.btn.setFixedSize(80, 25)
		self.btn.addItem("Postfixes", 22)
		self.btn.addItem("Base", "A string")
		self.btn.addItem("Item 03", "A string")
		self.btn.addItem("Item 04", "A string")
		self.btn.setStyleSheet(self.Style_comboBox)
		
		self.add_lineEdit = CustumeLineEditorWidget("Name", 80, 25)
		
		self.add_buttin = QtWidgets.QPushButton("+")
		self.add_buttin.setFixedSize(25, 25)
		self.add_buttin.setStyleSheet(self.Style_btn)
	
	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignHCenter)
		
		self.main_layout.addWidget(self.add_lineEdit)
		self.main_layout.addWidget(self.add_buttin)
		self.main_layout.addWidget(self.btn)
	
	def create_connections(self):
		pass
	
	def generate_random_color(self):
		# Генерируем случайные значения для R, G, B
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		
		# Формируем строку цвета в формате hex (#RRGGBB)
		color = f"#{r:02x}{g:02x}{b:02x}"
		return color
