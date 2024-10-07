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
		self.resources = Resources.get_instance()
		self.QSettings = QtCore.QSettings(self.resources.config_path, QtCore.QSettings.IniFormat)
		self.FixedHeigt = 200

		self.mode_button = self.QSettings.value("startup/mode_button", False)
		self.mode_number = self.QSettings.value("startup/mode_number", False)
		self.start_number = self.QSettings.value("startup/start_number", 1)
		self.padding_number = self.QSettings.value("startup/padding_number", 2)
		self.position_number =  self.QSettings.value("startup/position_number", 0)
		self.number = self.handle_number() #self.QSettings.value("startup/number", 10)
		self.prefix, self.suffix = self.handle_prefix_suffix()
		self.maxRange = 0
		self.minRange = 0
		self.cursor_pos = 0
		self.old_Text = ""




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
		self.LabelWidget.number_mode.changeStateNumberMode.connect(self.on_click_number_mode_button)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.textEdited.connect(self.do_text_edited)
		self.NumberWidget.new_number_Signal.connect(self.update_number)
		self.NumberWidget.new_position_Signal.connect(self.update_position_number)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.cursorPositionChanged.connect(self.posNumber_cursor)

	def update_position_number(self, value):
		self.position_number = value
		print(f"update position number {value}")

	def update_number(self, start_number, padding_number, number):
		self.start_number = start_number
		self.padding_number = padding_number
		self.number = number

		print(f'New number: {self.number}, start: {self.start_number}, padding: {self.padding_number}')

	def on_click_number_mode_button(self, state):
		self.NumberWidget.set_state_from_number_mode(state)
		self.mode_number = state
		self.number = self.handle_number()
		# self.state_number(state)
		print(f"Number mode  {state}: '{self.number}'")

	def state_number(self, state):

		Number = self.number
		name = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()
		start = self.position_number
		end = start + len(Number)
		left_text = name[:start]

		right_text = name[end:]
		print(right_text,"Right")
		sectionText = name[start:end]
		# cursor_pos =  self.position_number #self.cursor_pos
		print(start, end, left_text, right_text)
		cursor_pos = self.cursor_pos

		if state:

			if cursor_pos in range(start, len(name) + 1):
				cursor_pos += len(Number)
				print("+",cursor_pos)

			right_text = name[start:]
			name_number = left_text + Number + right_text
			print("QWEFQWEFQW",name_number)

			if name:
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(name_number)
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(cursor_pos)

				self.old_Text = name_number

		else:

			if cursor_pos in range(end, len(name) + 1):
				cursor_pos -= len(Number)
				print("-",cursor_pos)

			name_no_number = left_text + right_text
			print(left_text, right_text)
			print(name_no_number,"QWEFQWEFQWEF")

			if name:
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(name_no_number)
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(cursor_pos)

				self.old_Text = name_no_number

	def handle_number(self):
		"""Procesing number"""
		if self.mode_number:
			number = ("0" * (self.padding_number - len(str(self.start_number)))) + str(self.start_number)
		else:
			number = ""
		return number


	#------------chelck
	def update_text_with_number(self, text, number, start, end, prefix, suffix):
		"""Обновление текста с учетом номера, префикса и суффикса"""
		# left_text = text[:start]
		# right_text = text[end:]
		left_text = text[len(prefix):start]
		right_text = text[end:end - len(suffix)]
		new_text = prefix + left_text + number + right_text + suffix

		self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(new_text)
		self.old_Text = new_text
		print("[{3}][{0}][{2}][{1}][{4}] Range = {5}".format(left_text, right_text, number, prefix, suffix, self.maxRange))
		return new_text

	def handle_prefix_suffix(self):
		"""Обработка префикса и суффикса"""
		if self.mode_button:
			pass
			# TODO add prefix _ suffix возможно сделать как получение числа, через клик кнопки будет меняться префикс.
			# prefix = self.prefix_Editline.text()
			# suffix = self.suffix_Editline.text()
		else:
			prefix = ""
			suffix = ""
		return prefix, suffix

	def do_text_edited(self, text):


		# print(f"textEdited '{text}',prefix '{self.prefix}',suffix '{self.suffix}', number '{self.number}', oldTextLine '{self.old_Text}'")

		old_text = self.old_Text
		start = self.position_number
		cursor_pos = self.cursor_pos
		Delete_number = ""
		end = self.position_number + len(self.number)

		left_text = text[:self.position_number]
		right_text = text[end:]
		sectionText = text[self.position_number:end]

		items_add = len(text) - len(old_text)
		items_removed = len(old_text) - len(text)

		self.maxRange = len(text) - len(self.number) - len(self.suffix)
		self.minRange = len(self.prefix)

		right_without_suffix = old_text[end:len(old_text) - len(self.suffix)]

		if len(text) > len(self.number) + len(self.prefix) + len(self.suffix) and old_text:
			if len(text) > len(old_text):  # items_add

				self.old_Text = text

				if sectionText != self.number or self.number == "" and cursor_pos <= self.position_number:  # items_add in left_text! [left_text] >|< (sectionText != [Number]) [right_text]

					self.position_number += items_add
					left_text = text[:self.position_number]
					right_text = text[self.position_number + len(self.number):]
					print("here!!!")


			elif len(text) < len(old_text):  # items_removed

				self.old_Text = text

				if sectionText != self.number or self.number == "" and cursor_pos < self.position_number:  # items_removed in left_text! [left_text] >|< (sectionText != [Number]) [right_text]

					self.position_number -= items_removed
					start = self.position_number
					end = start + len(self.number)
					left_text = text[:start]
					right_text = text[end:]
					sectionText = text[start:end]

					if start < 0 + len(self.prefix) and 0 + len(self.prefix) != cursor_pos:  # start cannot to be negative  |  [-1][number]|[right_text]

						Delete_number = "Delete number, left negative"

						start = 0 + len(self.prefix)
						end = start + len(self.number)

						left_text = old_text[:start]
						right_text = old_text[end:]
						sectionText = old_text[start:end]

						self.maxRange = len(old_text) - len(self.number) - len(self.suffix)

						self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(old_text)
						self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(end)

					elif self.prefix != text[:len(self.prefix)]:

						Delete_number = "Delete prefix, left negative"

						self.position_number += items_removed
						start = self.position_number
						end = start + len(self.number)

						left_text = old_text[:start]
						right_text = old_text[end:]
						sectionText = old_text[start:end]

						self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(old_text)
						self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(len(self.prefix))
						self.maxRange = len(old_text) - len(self.number) - len(self.suffix)

					elif right_without_suffix == "" and sectionText != self.number and start + 1 == cursor_pos:  # end cannot to be negative  |  [number]|[][_suffix]

						Delete_number = "Delete number, right negative"

						self.position_number += items_removed
						start = self.position_number
						end = start + len(self.number)

						left_text = old_text[:start]
						right_text = old_text[end:]
						sectionText = old_text[start:end]

						self.maxRange = len(old_text) - len(self.number) - len(self.suffix)
						self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(old_text)
						self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(cursor_pos)
						right_without_suffix = "Delete number, right negative"

					if sectionText != self.number:  # [Text]DEL====>[Number]<===DEL[Text] Delet Number!

						self.position_number += items_removed
						start = self.position_number
						end = start + len(self.number)

						if start == cursor_pos:  # [Text]>>DEL>>|[Number][(T)ext] Delet Number!

							Delete_number = "Delete number , right"
							left_text = old_text[:start]
							right_text = old_text[end + items_removed:]
							NewText = left_text + self.number + right_text

							self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(NewText)
							self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(start)
							self.old_Text = NewText

							if right_text == "":
								self.maxRange = len(NewText) - len(self.number)

						else:  # self.End_index_number <= self.cursor_pos: # [Tex(t)][Number]|<<<DEL<<<[Text] Delet Number!

							self.position_number -= items_removed
							Delete_number = "Delete number, left"

							left_text = old_text[:start - items_removed]
							right_text = old_text[end:]
							NewText = left_text + self.number + right_text

							start = self.position_number
							end = start + len(self.number)

							self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(NewText)
							self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(end)
							self.old_Text = NewText

					else:

						if self.position_number <= 0 + len(
								self.prefix):  # start cannot be negative  |  [-1][number]|[right_text]
							self.position_number = 0 + len(self.prefix)
							self.old_Text = old_text
						elif cursor_pos == len(self.prefix) and self.prefix != text[:len(self.prefix)]:

							self.old_Text = old_text

						elif right_without_suffix == "Delete number, right negative":
							self.old_Text = old_text

						else:
							self.old_Text = text

				elif self.suffix != text[len(text) - len(self.suffix):]:

					Delete_number = "Delete suffix, right negative"

					self.maxRange = len(old_text) - len(self.number) - len(self.suffix)

					self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(old_text)
					self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(cursor_pos)

					self.old_Text = old_text

		else:

			if len(text) == len(self.number) + len(self.prefix) + len(self.suffix) or len(text) == 0:

				self.RenameWidget.LineEditor.AutoComplete_line_edit.setText("")
				self.old_Text = ""
				left_text = ""
				right_text = ""
				self.number = ""
				self.maxRange = 0
				Delete_number = "removed Number"
				self.position_number = 0

			else:

				self.maxRange = len(text) + len(self.prefix)
				self.position_number = len(text) + len(self.prefix)
				start = self.position_number
				Delete_number = "add Number"
				left_text = self.prefix + text
				right_text = "" + self.suffix

				NewText = self.prefix + text + self.number + self.suffix

				self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(NewText)
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(start)

				self.old_Text = NewText

		left_text = left_text[len(self.prefix):]
		right_text = right_text[:len(right_text) - len(self.suffix)]

		print("[{3}][{0}][{2}][{1}][{4}] Range = {5} {6}".format(left_text, right_text, self.number, self.prefix, self.suffix, self.maxRange,Delete_number))

		self.NumberWidget.index_slider.setRange(self.minRange, self.maxRange)
		self.NumberWidget.index_SpinBox.setRange(self.NumberWidget.index_slider.minimum(), self.NumberWidget.index_slider.maximum())
		self.NumberWidget.index_slider.setValue(self.position_number)
		self.NumberWidget.index_SpinBox.setValue(self.position_number)

		self.number = self.handle_number()

		# prefix, suffix = self.handle_prefix_suffix(text)
		#
		# if self.mode_number:
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
		# if len(text) > len(number) + len(prefix) + len(suffix) and self.old_Text:
		#
		# 	if len(text) > len(self.old_Text):  # items_add
		# 		self.old_Text = text
		# 		if text[start:end] != number and cursor_pos <= start:
		# 			self.start_number += len(text) - len(self.old_Text)
		# 			self.update_text_with_number(text, number, start, end, prefix, suffix)
		#
		# 	elif len(text) < len(self.old_Text):  # items_removed
		# 		self.old_Text = text
		# 		if text[start:end] != number and cursor_pos < start:
		# 			self.start_number -= len(self.old_Text) - len(text)
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


	def posNumber_cursor(self, oldPos, newPos):

		MineDataName = self.RenameWidget.LineEditor.AutoComplete_line_edit.oldMineData
		name = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()

		if name != MineDataName:
			self.prefix, self.suffix = self.handle_prefix_suffix()

			prefix = self.prefix
			suffix = self.suffix
			Number = self.number
			self.cursor_pos = newPos

			start = self.position_number
			end = start + len(Number)

			if MineDataName:
				print(MineDataName)
				if MineDataName in name:
					print(name)
					SplitName = name.split(MineDataName)
					name = SplitName[0] + SplitName[1]

			if newPos in range(start + 1, end):
				if oldPos >= end:

					self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(start)

				elif oldPos <= self.position_number:

					self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(end)
				print("number")

			if prefix:
				if newPos in range(0, len(prefix)):
					self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(len(prefix))
					print("prefix")

			if suffix:

				no_suffix = len(name) - len(suffix)

				if newPos in range(no_suffix + 1, len(name)) or newPos >= len(name):
					self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(no_suffix)
					print("suffix")