try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.CustumeLineEditorWidget import CustumeLineEditorWidget

class addSubCategoryWidget(QtWidgets.QWidget):
	isSubCategoryName = QtCore.Signal(str, str)
	
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
	
	def __init__(self, state, parent=None):
		super(addSubCategoryWidget, self).__init__(parent)
		# Modul---------------------------
		self.resources = Resources.get_instance()
		# Attribute---------------------------
		self.state           = state
		self.word_list       = list(self.resources.get_key_name_JSON("ListName"))
		self.currentCategory = self.resources.config.get_variable("library", "current_category", "Postfixes", str)
		# Setting---------------------------
		self.setFixedHeight(25)
		self.setVisible(self.state)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
		self.add_item_combobox()

	def create_widgets(self):
		self.combobox = QtWidgets.QComboBox()
		self.combobox.setFixedSize(80, 25)
		self.combobox.setStyleSheet(self.Style_comboBox)
		
		self.add_lineEdit = CustumeLineEditorWidget("Name", 80, 25)
		self.add_button   = QPushButtonAddName("+")
	
	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignHCenter)
		
		self.main_layout.addWidget(self.add_lineEdit)
		self.main_layout.addWidget(self.add_button)
		self.main_layout.addWidget(self.combobox)
	
	def create_connections(self):
		self.add_button.clicked.connect(self.on_clicked)
		self.combobox.currentTextChanged.connect(self.update_text)
		self.add_lineEdit.returnPressed.connect(self.on_clicked)
		
	def on_clicked(self):
		category = self.currentCategory
		name     = self.add_lineEdit.text()
		self.isSubCategoryName.emit(name, category)

		
		
	def update_text(self, text):
		self.currentCategory = text
		self.resources.config.set_variable("library", "current_category", text)
		
	def add_item_combobox(self, Delete_name = None):
		self.combobox.blockSignals(True)
		self.combobox.clear()
		if self.word_list:
			for i in self.word_list:
				self.combobox.addItem(i)
			
			if self.currentCategory not in self.word_list:
				newCarentCategory = self.word_list[0]
				self.update_text(text=newCarentCategory)

		if Delete_name:
			if self.currentCategory == Delete_name:
				if self.word_list:
					newCarentCategory = self.word_list[0]
					self.update_text(text = newCarentCategory)
				else:
					self.update_text(text = None)
					
		self.combobox.setCurrentText(self.currentCategory)
		self.combobox.blockSignals(False)


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