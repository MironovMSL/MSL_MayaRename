try:
    from PySide2 import QtWidgets, QtGui, QtCore
    from PySide2.QtWidgets import QAction
except:
    from PySide6 import QtWidgets, QtGui, QtCore
    from PySide6.QtGui import QAction


class CustomButtonLibrary(QtWidgets.QPushButton):

	itClickedName = QtCore.Signal(str)
	Style_btn = """
		    QPushButton {
		        background-color: rgb(50, 50, 50); /* Темно-серый фон */
		        border-style: outset;
		        border-width: 2px;
		        border-radius: 8px;
		        border-color: rgb(30, 30, 30); /* Темнее границы */
		        font: normal 12px; /* Жирный шрифт */
		        font-family: Roboto; /* Шрифт Arial */ Helvetica, Calibri, Verdana, Tahoma, Segoe UI, Open Sans, Roboto, Source Sans Pro
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
	# Style_btn = """
	#     QPushButton {
	#         background-color: rgb(60, 60, 60); /* Более светлый темно-серый фон */
	#         border-style: outset;
	#         border-width: 2px;
	#         border-radius: 8px; /* Более выраженные закругленные углы */
	#         border-color: rgb(40, 40, 40); /* Темнее границы */
	#         font: normal 12px;
	#         font-family: Roboto;/* Шрифт Arial */ Arial, Helvetica, Calibri, Verdana, Tahoma, Segoe UI, Open Sans, Source Sans Pro;
	#         color: rgb(210, 210, 210); /* Светло-серый текст */
	#         padding: 0px 0px; /* Внутренние отступы */
	#         box-shadow: 2px 2px 5px rgba(0, 0, 0, 80); /* Легкая тень */
	#     }
	#     QPushButton:hover {
	#         border-color: rgb(90, 90, 90); /* Светлее граница при наведении */
	#         background-color: rgb(100, 100, 100); /* Еще более светлый серый при наведении */
	#         color: rgb(255, 255, 255); /* Белый текст при наведении */
	#     }
	#     QPushButton:pressed {
	#         background-color: rgb(40, 40, 40); /* Темный фон при нажатии */
	#         border-style: inset; /* Впадение при нажатии */
	#         color: rgb(230, 230, 230); /* Почти белый текст при нажатии */
	#     }
	# """

	Style_lineEdit = """
	    QLineEdit {
	        background-color: rgb(70, 70, 250); /* Темно-серый фон */
	        border: 2px solid rgb(40, 40, 40); /* Темная граница */
	        border-radius: 8px; /* Закругленные углы */
	        font: normal 12px;
	        font-family: Roboto; /* Шрифт Arial */ Arial, Helvetica, Calibri, Verdana, Tahoma, Segoe UI, Open Sans, Source Sans Pro;
	        color: rgb(210, 210, 210); /* Светло-серый текст */
	        padding: 0px 0px; /* Внутренние отступы */
	    }
	    QLineEdit:hover {
	        border: 2px solid rgb(150, 150, 200); /* Светлее граница при наведении */
	        background-color: rgb(70, 70, 100); /* Немного светлее фон при наведении */
	    }
	    QLineEdit:focus {
	        border: 2px solid rgb(150, 150, 250); /* Синяя граница при фокусе */
	        background-color: rgb(70, 70, 150); /* Немного светлее фон при фокусе */
	    }
	"""


	def __init__(self, name="", width = 40, height = 25, parent=None):
		super(CustomButtonLibrary, self).__init__(parent)
		
		# Attribute---------------------------
		self.name   = name
		self.width  = width
		self.height = height
		# Setting---------------------------
		self.setFixedSize(self.width, self.height)
		self.setText(self.name)
		self.setStyleSheet(self.Style_btn)
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()

	def create_widgets(self):
		self.rename_lineEdit = QtWidgets.QLineEdit()
		self.rename_lineEdit.setStyleSheet(self.Style_lineEdit)
		self.rename_lineEdit.setText(self.name)
		self.rename_lineEdit.setAlignment(QtCore.Qt.AlignHCenter)
		self.rename_lineEdit.setVisible(0)
		self.rename_lineEdit.setFixedHeight(25)

	def create_layouts(self):
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.main_layout.addWidget(self.rename_lineEdit)

	def create_connections(self):
		self.rename_lineEdit.returnPressed.connect(self.setNewMame)
		self.clicked.connect(self.on_clicked)

	def on_clicked(self):
		print(f"TODO: clocked {self.name}")
		self.itClickedName.emit(self.text())

	def setNewMame(self):

		btnText = self.text()
		text = self.rename_lineEdit.text()
		self.name = text
		self.setText(text)

		self.Rename_bnt()

		print("Rename button [{}] in [{}]".format(btnText, text))

	def enterEvent(self, event):
		self.setCursor(QtCore.Qt.PointingHandCursor)
		super(CustomButtonLibrary, self).enterEvent(event)

	def leaveEvent(self, event):
		self.setCursor(QtCore.Qt.ArrowCursor)
		super(CustomButtonLibrary, self).leaveEvent(event)

	def mouseReleaseEvent(self, event):
		super(CustomButtonLibrary, self).mouseReleaseEvent(event)
		self.itClickedName.emit(self.text())

	def mousePressEvent(self, event):

		super(CustomButtonLibrary, self).mousePressEvent(event)
		if event.buttons() == QtCore.Qt.RightButton:
			self.creat_context_menu()
			self.popMenu.exec_(self.mapToGlobal(event.pos()))

		if hasattr(QtCore.Qt, "MiddleButton"):
			middle_button = QtCore.Qt.MiddleButton  # Для Qt6
		else:
			middle_button = QtCore.Qt.MidButton  # Для Qt5

		if event.buttons() != middle_button:
			return

		self.setVisible(0)
		mimeData = NameMIMEData()
		mimeData.Name_Btn = self.text()

		# Creat ghost image
		self.pixmap = self.grab()
		painter = QtGui.QPainter(self.pixmap)

		painter.setCompositionMode(painter.CompositionMode_DestinationIn)
		painter.fillRect(self.pixmap.rect(), QtGui.QColor(80, 80, 80, 100))
		painter.end

		# start drag and drop
		drag = QtGui.QDrag(self)
		drag.setMimeData(mimeData)
		drag.setPixmap(self.pixmap)
		drag.setHotSpot(event.pos())

		drag.exec_(QtCore.Qt.LinkAction | QtCore.Qt.MoveAction)

	def creat_context_menu(self):

		self.popMenu = QtWidgets.QMenu(self)

		self.popMenuAdd = QAction("Rename", self)
		self.popMenu.addAction(self.popMenuAdd)
		self.popMenuAdd.triggered.connect(self.Rename_bnt)

		self.popMenuDel = QAction("Delete", self)
		self.popMenu.addAction(self.popMenuDel)
		self.popMenuDel.triggered.connect(self.Delete_btn)

	def Rename_bnt(self):
		vis = self.rename_lineEdit.isVisible()
		if vis:
			self.rename_lineEdit.setVisible(0)

		else:
			self.rename_lineEdit.setVisible(1)
			self.rename_lineEdit.setFocus()

	def Delete_btn(self):
		self.deleteLater()
		print("Delete button [{}]".format(self.text()))