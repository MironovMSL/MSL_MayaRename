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

class LineEditorWidget(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(LineEditorWidget, self).__init__(parent)

		# Attribute---------------------------
		self.resource: Resources = Resources.get_instance()
		self.word_list = self.resource.all_item_json # list of all words library.

		# Run function---------------------------
		self.create_widgets()
		self.create_layouts()

	def create_widgets(self):

		self.completer = CustomCompleter(self.word_list)
		self.AutoComplete_line_edit = AutoCompleteLineEdit(self.completer, self)
		self.model = QtCore.QStringListModel()  # model for list name.

		# List of words for autocompletion
		self.completer.setModel(self.model)
		self.model.setStringList(self.word_list)

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

	def __init__(self, completer, parent=None):
		super(AutoCompleteLineEdit, self).__init__(parent)

		# Attribute---------------------------
		Width            = 200
		Height           = 25
		NameHolder       = "Name"
		ToolTip          = "Texting edit for Rename"
		Font             = QtGui.QFont("Arial", 10, QtGui.QFont.Normal)
		self.completer   = completer
		self.oldCursor   = self.cursorPosition()
		self.oldMineData = ""

		# Setting---------------------------
		self.setFixedHeight(Height)
		self.setMinimumWidth(Width)
		self.setPlaceholderText(NameHolder)
		self.setToolTip(ToolTip)
		self.setFont(Font)
		self.setCompleter(self.completer)
		self.setAttribute(QtCore.Qt.WA_InputMethodEnabled)
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.setClearButtonEnabled(True)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.installEventFilter(self)
		self.setStyleSheet(self.Style_lineEdit)
		#---------------------------
		self.create_connections()

	def create_connections(self):
		self.textEdited.connect(self.on_text_edited)

	def on_text_edited(self, text):
		self.completer.update_completer(text) # Update the compliterator when the text changes

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Tab:  # Checking the TAB key press

			filtered_words = self.completer.model().stringList()  # We get a list of words (w..) -->[wrist, wing]
			if filtered_words:  # If there are matches
				current_index = self.completer.popup().currentIndex()
				if not current_index.isValid():
					completion = filtered_words[0]  # We take the first match
					cursor_pos = self.cursorPosition()
					text = self.text()
					new_text = text[:text.rfind('_') + 1] + completion # Replace part of the text with autocomplete
					self.setText(new_text)
					self.setCursorPosition(len(new_text))  # Place the cursor at the end
			self.completer.popup().hide()
			event.accept()  # Stop further processing TAB
			return
		super().keyPressEvent(event)

	def focusNextPrevChild(self, next): # Intercept focusNextPrevChild to prevent focus switching
		return False # Stop focus switching when pressing TAB

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

class CustomCompleter(QtWidgets.QCompleter):
	def __init__(self, words, parent=None):
		QtWidgets.QCompleter.__init__(self, parent)

		self.words = words

		self.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)  # PopupCompletion , InlineCompletion , UnfilteredPopupCompletion
		self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.setWrapAround(False)

	def update_completer(self, text):
		parts = text.split('_')
		if len(parts) > 1:
			prefix = parts[-1]  # Use the part after the last '_'
			if not prefix:  # If there is nothing after '_', we don't show the hint
				self.model().setStringList([])
				return
		else:
			prefix = text  # If there is no '_', use the whole text

		filtered_words = [word for word in self.words if word.startswith(prefix)] # Filter words based on prefix
		self.model().setStringList(filtered_words)

	def pathFromIndex(self, index):
		path = QtWidgets.QCompleter.pathFromIndex(self, index) # Get the selected word [name]
		lst = str(self.widget().text()).split('_') # We get a list of words split by '_' [name, prefix, name]
		if len(lst) > 1:
			path = f"{'_'.join(lst[:-1])}_{path}" # Replace part of the word on the selected word in autocomplete
		return path

	def splitPath(self, path):
		PATH = str(path.split('_')[-1]).lstrip(' ') # get the last word after '_' [prefix_name_se] ---> [se]
		return [PATH]