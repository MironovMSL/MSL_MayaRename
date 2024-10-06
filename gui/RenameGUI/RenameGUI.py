from sys import prefix

try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.gui.RenameGUI.FunctionWidget.FunctionWidget import FunctionWidget
from MSL_MayaRename.gui.RenameGUI.RenameWidget.RenameWidget import RenameWidget
from MSL_MayaRename.gui.RenameGUI.NumberWidget.NumberWidget import NumberWidget
from MSL_MayaRename.gui.RenameGUI.LetterWidget.LetterWidget import LetterWidget
from MSL_MayaRename.gui.RenameGUI.SuffixPrefixWidget.SuffixPrefixWidget import SuffixPrefixWidget
from MSL_MayaRename.gui.RenameGUI.LabelWidget.LabelWidget import LabelWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonName.QuickListButtonName import QuickListButtonName
from MSL_MayaRename.gui.RenameGUI.CasheNameWidget.CasheNameWidget import CasheNameWidget

import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__)

class RenameGUI(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(RenameGUI, self).__init__(parent)

		# Attribute----------------------
		self.FixedHeigt = 200
		self.resources :Configurator = Resources.get_instance()

		self.button_mode = self.resources.config.get_variable("startup", "mode_button", False)
		self.number_mode = self.resources.config.get_variable("startup", "mode_number", False)
		self.start_number = self.resources.config.get_variable("startup", "start_number", 1)
		self.padding_number = self.resources.config.get_variable("startup", "padding_number", 2)
		self.position_number =  self.resources.config.get_variable("startup", "position_number", 0)
		self.number = self.handle_number()
		self.maxRange = 0
		self.minRange = 0
		self.oldTextLine = ""
		self.cursor_pos = 0
		self.prefix = ""
		self.suffix = ""
		self.old_prefix = ""
		self.old_suffix = ""


		# Setting ------------------------
		self.setFixedHeight(self.FixedHeigt)
		# Run function ------------------------
		self.create_Widgets()
		self.create_layouts()
		self.create_connections()

	def create_Widgets(self):

		self.FunctionWidget = FunctionWidget()
		self.LabelWidget = LabelWidget()
		self.RenameButton = QtWidgets.QPushButton("Rename")
		self.RenameButton.setFixedSize(50, 75)
		self.RenameWidget = RenameWidget()
		self.NumberWidget = NumberWidget()
		self.LetterWidget = LetterWidget()
		self.SuffixPrefixWidget = SuffixPrefixWidget()
		self.QuickListButtonName = QuickListButtonName()
		self.CasheNameWidget = CasheNameWidget()

	def create_layouts(self):
		# main layout
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		# left and Right layout for widgets ---> RenameWidget, NumberWidget, LetterWidget,
		self.main_rename_layout = QtWidgets.QHBoxLayout()
		self.main_rename_layout.setContentsMargins(0, 0, 0, 0)
		self.main_rename_layout.setSpacing(0)

		self.left_layout = QtWidgets.QVBoxLayout()
		self.left_layout.setContentsMargins(0, 0, 0, 0)
		self.left_layout.setSpacing(0)
		self.Right_lyout = QtWidgets.QVBoxLayout()
		self.Right_lyout.setContentsMargins(0, 0, 0, 0)
		self.Right_lyout.setSpacing(0)

		self.main_rename_layout.addLayout(self.left_layout)
		self.main_rename_layout.addLayout(self.Right_lyout)

		# add LabelWidget RenameWidget, NumberWidget, LetterWidget, RenameButton, SuffixPrefixWidget, QuickListButtonName
		self.main_layout.addWidget(self.FunctionWidget)
		self.main_layout.addWidget(self.LabelWidget)
		self.main_layout.addLayout(self.main_rename_layout)
		self.left_layout.addWidget(self.RenameWidget)
		self.left_layout.addWidget(self.NumberWidget)
		self.left_layout.addWidget(self.LetterWidget)
		self.Right_lyout.addWidget(self.RenameButton)
		self.main_layout.addWidget(self.SuffixPrefixWidget)
		self.main_layout.addWidget(self.QuickListButtonName)
		self.main_layout.addWidget(self.CasheNameWidget)

		self.main_layout.addStretch()

	def create_connections(self):
		self.LabelWidget.number_mode.changeStateNumberMode.connect(self.on_number_mode_button_click)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.textEdited.connect(self.do_text_edited)
		# self.RenameWidget.LineEditor.AutoComplete_line_edit.cursorPositionChanged.connect(self.posNumber_cursor)
		# self.lineEdit_rename.itDropName.connect(self.text_edited)
		# self.lineEdit_rename.returnPressed.connect(self.slidLineEdit)

		# self.NumberWidget.number_start.valueChanged.connect(self.set_number_text)
		# self.NumberWidget.number_padding.valueChanged.connect(self.set_number_text)
		# self.NumberWidget.index_SpinBox.valueChanged.connect(self.on_spinBox_value)
		# self.NumberWidget.index_slider.sliderMoved.connect(self.on_slider_move_value)


	def on_number_mode_button_click(self, state):
		self.NumberWidget.set_state_from_number_mode(state)
		self.number_mode = state
		self.number = self.handle_number()
		print(self.number,"print number from state")

	def handle_number(self):
		"""Procesing number"""
		if self.number_mode:
			number = ("0" * (self.padding_number - len(str(self.start_number)))) + str(self.start_number)
		else:
			number = ""
		return number


	#------------chelck
	def update_text_with_number(self, text, number, start, end, prefix, suffix):
		"""Обновление текста с учетом номера, префикса и суффикса"""
		left_text = text[:start]
		right_text = text[end:]
		new_text = prefix + left_text + number + right_text + suffix

		self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(new_text)
		self.oldTextLine = new_text
		return new_text

	def handle_prefix_suffix(self):
		"""Обработка префикса и суффикса"""
		if self.button_mode:
			pass
			# TODO add prefix _ suffix возможно сделать как получение числа, через клик кнопки будет меняться префикс.
			# prefix = self.prefix_Editline.text()
			# suffix = self.suffix_Editline.text()
		else:
			prefix = ""
			suffix = ""
		return prefix, suffix

	def do_text_edited(self, text):
		print(f"TODO : Rename GUI textEdited: {text}")

		self.prefix, self.suffix = self.handle_prefix_suffix()
		self.number = self.handle_number()
		# self.RenameWidget.LineEditor.AutoComplete_line_edit.setText()
		prefix = self.prefix
		suffix = self.suffix
		Number = self.number
		old_text = self.oldTextLine
		start = self.position_number
		cursor_pos = self.cursor_pos
		Delete_number = ""
		end = start + len(Number)
		left_text = text[:start]
		right_text = text[end:]
		sectionText = text[start:end]
		items_add = len(text) - len(old_text)
		items_removed = len(old_text) - len(text)
		self.maxRange = len(text) - len(Number) - len(suffix)
		self.minRange = len(prefix)
		right_without_suffix = old_text[end:len(old_text) - len(suffix)]

		if len(text) > len(Number) + len(prefix) + len(suffix) and old_text:

			if len(text) > len(old_text):  # items_add

				self.oldTextLine = text

				if sectionText != Number or Number == "" and cursor_pos <= start:  # items_add in left_text! [left_text] >|< (sectionText != [Number]) [right_text]

					self.position_number += items_add
					start = self.position_number
					end = start + len(Number)
					left_text = text[:start]
					right_text = text[end:]

			elif len(text) < len(old_text):  # items_removed

				self.oldTextLine = text

				if sectionText != Number or Number == "" and cursor_pos < start:  # items_removed in left_text! [left_text] >|< (sectionText != [Number]) [right_text]

					self.position_number -= items_removed
					start = self.position_number
					end = start + len(Number)
					left_text = text[:start]
					right_text = text[end:]
					sectionText = text[start:end]

					if start < 0 + len(prefix) and 0 + len(
							prefix) != cursor_pos:  # start cannot to be negative  |  [-1][number]|[right_text]

						Delete_number = "Delete number, left negative"

						start = 0 + len(prefix)
						end = start + len(Number)

						left_text = old_text[:start]
						right_text = old_text[end:]
						sectionText = old_text[start:end]

						self.maxRange = len(old_text) - len(Number) - len(suffix)

						self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(old_text)
						self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(end)

					elif prefix != text[:len(prefix)]:

						Delete_number = "Delete prefix, left negative"

						self.position_number += items_removed
						start = self.position_number
						end = start + len(Number)

						left_text = old_text[:start]
						right_text = old_text[end:]
						sectionText = old_text[start:end]

						self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(old_text)
						self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(len(prefix))
						self.maxRange = len(old_text) - len(Number) - len(suffix)

					elif right_without_suffix == "" and sectionText != Number and start + 1 == cursor_pos:  # end cannot to be negative  |  [number]|[][_suffix]

						Delete_number = "Delete number, right negative"

						self.position_number += items_removed
						start = self.position_number
						end = start + len(Number)

						left_text = old_text[:start]
						right_text = old_text[end:]
						sectionText = old_text[start:end]

						self.maxRange = len(old_text) - len(Number) - len(suffix)
						self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(old_text)
						self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(cursor_pos)
						right_without_suffix = "Delete number, right negative"

					if sectionText != Number:  # [Text]DEL====>[Number]<===DEL[Text] Delet Number!

						self.position_number += items_removed
						start = self.position_number
						end = start + len(Number)

						if start == cursor_pos:  # [Text]>>DEL>>|[Number][(T)ext] Delet Number!

							Delete_number = "Delete number , right"
							left_text = old_text[:start]
							right_text = old_text[end + items_removed:]
							NewText = left_text + Number + right_text

							self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(NewText)
							self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(start)
							self.oldTextLine = NewText

							if right_text == "":
								self.maxRange = len(NewText) - len(Number)

						else:  # self.End_index_number <= self.cursor_pos: # [Tex(t)][Number]|<<<DEL<<<[Text] Delet Number!

							self.position_number -= items_removed
							Delete_number = "Delete number, left"

							left_text = old_text[:start - items_removed]
							right_text = old_text[end:]
							NewText = left_text + Number + right_text

							start = self.position_number
							end = start + len(Number)

							self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(NewText)
							self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(end)
							self.oldTextLine = NewText

					else:

						if self.position_number <= 0 + len(
								prefix):  # start cannot be negative  |  [-1][number]|[right_text]
							self.position_number = 0 + len(prefix)
							self.oldTextLine = old_text
						elif cursor_pos == len(prefix) and prefix != text[:len(prefix)]:

							self.oldTextLine = old_text

						elif right_without_suffix == "Delete number, right negative":
							self.oldTextLine = old_text

						else:
							self.oldTextLine = text

				elif suffix != text[len(text) - len(suffix):]:

					Delete_number = "Delete suffix, right negative"

					self.maxRange = len(old_text) - len(Number) - len(suffix)

					self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(old_text)
					self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(cursor_pos)

					self.oldTextLine = old_text

		else:

			if len(text) == len(Number) + len(prefix) + len(suffix) or len(text) == 0:

				self.RenameWidget.LineEditor.AutoComplete_line_edit.setText("")
				self.oldTextLine = ""
				left_text = ""
				right_text = ""
				Number = ""
				self.maxRange = 0
				Delete_number = "removed Number"
				self.position_number = 0

			else:

				self.maxRange = len(text) + len(prefix)
				self.position_number = len(text) + len(prefix)
				start = self.position_number
				Delete_number = "add Number"
				left_text = prefix + text
				right_text = "" + suffix

				NewText = prefix + text + Number + suffix

				self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(NewText)
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(start)

				self.oldTextLine = NewText

		left_text = left_text[len(prefix):]
		right_text = right_text[:len(right_text) - len(suffix)]

		print("[{3}][{0}][{2}][{1}][{4}] Range = {5} {6}".format(left_text, right_text, Number, prefix, suffix, self.maxRange,Delete_number))

		# self.index_slider.setRange(self.minRange, self.maxRange)
		# self.index_SpinBox.setRange(self.index_slider.minimum(), self.index_slider.maximum())
		#
		# self.index_slider.setValue(self.position_number)
		# self.index_SpinBox.setValue(self.position_number)

		self.NumberWidget.index_slider.setRange(self.minRange, self.maxRange)
		self.NumberWidget.index_SpinBox.setRange(self.NumberWidget.index_slider.minimum(), self.NumberWidget.index_slider.maximum())
		self.NumberWidget.index_slider.setValue(self.position_number)
		self.NumberWidget.index_SpinBox.setValue(self.position_number)

		# prefix, suffix = self.handle_prefix_suffix(text)
		#
		# if self.number_mode:
		# 	number = self.NumberText
		#
		# else:
		# 	number = ""
		#
		# start = self.position_number
		# cursor_pos = self.cursor_pos
		# end = start + len(number)
		#
		# left_text = text[:start]
		# right_text = text[end:]
		# print(left_text, right_text)
		#
		# if len(text) > len(number) + len(prefix) + len(suffix) and self.oldTextLine:
		#
		# 	if len(text) > len(self.oldTextLine):  # items_add
		# 		self.oldTextLine = text
		# 		if text[start:end] != number and cursor_pos <= start:
		# 			self.start_number += len(text) - len(self.oldTextLine)
		# 			self.update_text_with_number(text, number, start, end, prefix, suffix)
		#
		# 	elif len(text) < len(self.oldTextLine):  # items_removed
		# 		self.oldTextLine = text
		# 		if text[start:end] != number and cursor_pos < start:
		# 			self.start_number -= len(self.oldTextLine) - len(text)
		# 			self.update_text_with_number(text, number, start, end, prefix, suffix)
		#
		# 	# Логика для работы с префиксами/суффиксами
		# 	if prefix != text[:len(prefix)]:
		# 		self.handle_prefix_change(text, prefix, number)
		# 	elif suffix != text[len(text) - len(suffix):]:
		# 		self.handle_suffix_change(text, suffix)
		#
		# self.maxRange = len(text) - len(self.NumberText) - len(suffix)
		# self.minRange = len(prefix)
		# print(self.minRange,self.maxRange)
		#
		# # Установление диапазона значений
		# self.NumberWidget.index_slider.setRange(self.minRange, self.maxRange)
		# self.NumberWidget.index_SpinBox.setRange(self.NumberWidget.index_slider.minimum(), self.NumberWidget.index_slider.maximum())
		# self.NumberWidget.index_slider.setValue(self.position_number)
		# self.NumberWidget.index_SpinBox.setValue(self.position_number)


