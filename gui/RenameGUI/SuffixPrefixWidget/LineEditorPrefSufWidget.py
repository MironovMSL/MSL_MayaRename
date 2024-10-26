try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.core.common import *
import os



class NameMIMEData(QtCore.QMimeData):
	def __init__(self, text=None):
		super(NameMIMEData, self).__init__()

		if text:
			self.Name_Btn = text
		else:
			self.Name_Btn = ""

class LineEditorPrefSufWidget(QtWidgets.QWidget):
	def __init__(self, NameHolder,Width, parent=None):
		super(LineEditorPrefSufWidget, self).__init__(parent)

		# Attribute---------------------------
		self.Width = Width
		self.NameHolder = NameHolder
		self.resource: Resources = Resources.get_instance()
		self.word_list = self.resource.all_item_json # list of all words library.


		# Run function---------------------------
		self.create_widgets()
		self.create_layouts()

	def create_widgets(self):

		self.AutoComplete_line_edit = AutoCompleteLineEdit(self.NameHolder,self.Width, self)


	def create_layouts(self):

		# main Layout
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# add widget
		self.main_layout.addWidget(self.AutoComplete_line_edit)


class AutoCompleteLineEdit(QtWidgets.QLineEdit):
	itDropName = QtCore.Signal(str, int)

	Style_lineEdit = """
	    QLineEdit {
	        background-color: rgb(40, 40, 40);  /* Темно-серый фон */
	        border: 2px solid rgb(70, 70, 70);  /* Серо-черная граница */
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

	def __init__(self, NameHolder, Width, parent=None):
		super(AutoCompleteLineEdit, self).__init__(parent)

		# Attribute---------------------------
		self.Width       = Width
		Height           = 25
		self.NameHolder  = NameHolder
		ToolTip          = "Texting edit for Rename"
		Font             = QtGui.QFont("Arial", 10, QtGui.QFont.Normal)
		# self.completer   = completer
		self.oldCursor   = self.cursorPosition()
		self.oldMineData = ""

		# Setting---------------------------
		self.setFixedHeight(Height)
		self.setMaximumWidth(self.Width)
		self.setPlaceholderText(self.NameHolder)
		self.setToolTip(ToolTip)
		self.setFont(Font)

		self.setAttribute(QtCore.Qt.WA_InputMethodEnabled)
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.setClearButtonEnabled(True)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.installEventFilter(self)
		self.setStyleSheet(self.Style_lineEdit)
		#---------------------------
		# self.create_connections()


	def dragLeaveEvent(self, event):
		text = self.text()
		Name = self.oldMineData

		if Name in text:
			splitText = text.split(Name)
			text = splitText[0] + splitText[1]
		self.setText(text)

	def dragEnterEvent(self, event):
		event.acceptProposedAction()

		mimeData = event.mimeData()

		if mimeData.hasText():
			Name = "[" + mimeData.text() + "]"
		elif hasattr(mimeData, 'Name_Btn'):
			Name = "[" + mimeData.Name_Btn + "]"
		else:
			Name = ""

		self.oldMineData = Name

		# More precise determination of the cursor position
		posC = self.cursorPositionAt(event.pos())

		self.setCursorPosition(posC)
		self.setFocus()

		pos = self.cursorPosition()
		text = self.text()
		NewText = text[:pos] + Name + text[pos:]  # Insert text with brackets when dragging
		self.oldCursor = pos
		self.setText(NewText)

	def dragMoveEvent(self, event):
		event.acceptProposedAction()
		posC = self.cursorPositionAt(event.pos())
		self.setCursorPosition(posC)

		pos  = self.cursorPosition()
		text = self.text()
		Name = self.oldMineData

		if self.oldCursor != pos:
			if Name in text:
				splitText = text.split(Name)
				Text = splitText[0] + splitText[1]
				NewText = Text[:pos] + Name + Text[pos:]
			else:
				NewText = text[:pos] + Name + text[pos:]

			self.oldCursor = pos
			self.setText(NewText)
			print(pos)

	def dropEvent(self, event):
		mimeData = event.mimeData()
		text     = self.text()
		pos_cur      = self.oldCursor

		if mimeData.hasText(): # Extract the original text without brackets
			Name = mimeData.text()  # Original text without brackets
		elif hasattr(mimeData, 'Name_Btn'):
			Name = mimeData.Name_Btn
		else:
			Name = ""


		if self.oldMineData in text: # Remove the text with brackets inserted earlier
			splitText = text.split(self.oldMineData)
			text = splitText[0] + splitText[1]

		if Name:
			NewText = text[:pos_cur] + Name + text[pos_cur:]  # Insert the original text without brackets
			self.oldMineData = ""
			self.setText(NewText)
			self.itDropName.emit(NewText, pos_cur)

		event.source().setVisible(True)
