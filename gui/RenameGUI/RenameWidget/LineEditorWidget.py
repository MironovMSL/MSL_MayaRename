try:
	from PySide6 import QtWidgets, QtGui, QtCore
except:
	from PySide2 import QtWidgets, QtGui, QtCore


import os
import maya.cmds as cmds


class LineEditorWidget(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(LineEditorWidget, self).__init__(parent)

		word_list = ["prefix", "name", "suffix", "maya", "node", "scene"]

		# ---------------------Create completer---------------------
		self.completer = CustomCompleter(word_list)
		model = QtCore.QStringListModel()
		# ---------------------List of words for autocompletion---------------------
		model.setStringList(word_list)
		self.completer.setModel(model)

		# ---------------------QLineEdit with autocompletion---------------------
		self.AutoComplete_line_edit = AutoCompleteLineEdit(self.completer, self)

		# ---------------------main Layout---------------------
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		# ---------------------add widget---------------------
		self.main_layout.addWidget(self.AutoComplete_line_edit)

class AutoCompleteLineEdit(QtWidgets.QLineEdit):

	def __init__(self, completer, parent=None):
		super().__init__(parent)

		# ---------------------Attribute ---------------------
		Width = 200
		Height = 25
		NameHolder = "Name"
		self.completer = completer

		# ---------------------Setting---------------------
		self.setFixedSize(Width, Height)
		self.setPlaceholderText(NameHolder)
		self.setFont(QtGui.QFont("Calibri", 11, QtGui.QFont.Normal))
		self.setCompleter(self.completer)
		self.setAttribute(QtCore.Qt.WA_InputMethodEnabled)
		self.setClearButtonEnabled(True)
		self.installEventFilter(self)

		# ---------------------connect---------------------
		self.textEdited.connect(self.on_text_edited)

	def on_text_edited(self, text):
		self.completer.update_completer(text) # Update the compliterator when the text changes

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Tab:  # Checking the TAB key press
			filtered_words = self.completer.model().stringList()  # We get a list of words []
			if filtered_words:  # If there are matches
				completion = filtered_words[0]  # We take the first match
				cursor_pos = self.cursorPosition()
				text = self.text()
				new_text = text[:text.rfind('_') + 1] + completion # Replace part of the text with autocomplete
				self.setText(new_text)
				self.setCursorPosition(len(new_text))  # Place the cursor at the end
				event.accept()  # Stop further processing TAB
				return
		super().keyPressEvent(event)

	def focusNextPrevChild(self, next): # Intercept focusNextPrevChild to prevent focus switching
		return False # Stop focus switching when pressing TAB

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
			path = '%s_%s' % ('_'.join(lst[:-1]), path) # Replace part of the word on the selected word in autocomplete
		return path

	def splitPath(self, path):
		path_ = path
		print(path_)
		path_ = str(path.split('_')[-1]).lstrip(' ') # get the last word after '_' [prefix_name_se] ---> [se]
		return [path_]




