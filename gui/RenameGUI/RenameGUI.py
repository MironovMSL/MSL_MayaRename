from lib2to3.main import diff_texts
from sys import prefix, int_info
from time import process_time_ns
from traceback import print_tb

from maya.cmds import reroot

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
from MSL_MayaRename.gui.RenameGUI.LabelWidget.LabelWidget import LabelWidget, new_root
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
		# mode----------------------------
		self.mode_button = None # mode number for button and lineEdits
		self.mode_number = None # mode number for Numeric
		# blocks text------------------------------------
		self.prefix = None  # [prefix]
		self.left = None # [left_text]
		self.X = None # [X] number or letter
		self.mid = None #[mid_text]
		self.Y = None # [Y] number or letter
		self.right = None #[right text]
		self.suffix = None  # [suffix]

		self.text = None # old text for comperisen [last Text]
		# number-----------------------------------
		self.pos_num = None  # position number [pos:end]
		self.end_pos_num = None # end position num [pos:end]
		self.num = None  # number start = 1, padding = 2, number = [01]
		# letter----------------------------------
		self.pos_let = None # position letter [pos:end]
		self.end_pos_let = None # end position letter [pos:end]
		self.let = None # letter  ~ [lettter]
		# Range and cursor-------------------------------
		self.pos_cur = None # cursor position for comparison
		self.maxR = None # maximum range for position [number] and [letter]
		self.minR = None # minimum range for position [number] and [letter]

		# Setting ------------------------
		self.setFixedHeight(self.FixedHeigt)
		# Run function ------------------------
		self.create_Widgets()
		self.create_layouts()
		self.create_connections()
		self.init_attribute()
		self.info_attribute()

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

	def init_attribute(self):

		# mode----------------------------
		self.mode_button = self.QSettings.value("startup/mode_button", False, bool)  # mode number for button and lineEdits
		self.mode_number = self.QSettings.value("startup/mode_number", False, bool)  # mode number for Numeric
		# number-----------------------------------
		self.start_num = self.QSettings.value("startup/start_number", 1, int)  # start number ~ 1
		self.padding_num = self.QSettings.value("startup/padding_number", 2, int)  # pading number ~ 2 = 00
		self.num = self.handle_number()  # number start = 1, padding = 2, number = [01]
		self.pos_num = self.QSettings.value("startup/position_number", 0, int)  # position number [pos:end]
		self.end_pos_num = self.pos_num + len(self.num)  # end position num [pos:end]
		self.num_cod = ""
		# letter----------------------------------
		self.pos_let = 0  # position letter [pos:end]
		self.end_pos_let = 0  # end position letter [pos:end]
		self.let = ""  # letter  ~ [lettter]
		self.let_cod = ""
		# Range and cursor-------------------------------
		self.pos_cur = 0  # cursor position for comparison
		self.maxR = 0  # maximum range for position [number] and [letter]
		self.minR = 0  # minimum range for position [number] and [letter]
		# blocks text------------------------------------
		self.text = ""  # old text for comperisen [last Text]
		self.prefix, self.suffix = self.handle_prefix_suffix()
		self.X, self.mid, self.Y = self.handle_X_mid_Y()
		self.left ,self.right = self.handle_left_right()
		#------------------------------
		self.info = "Initialization attribute"

	def get_end_pos(self, pos, name):
		end_pos = pos + len(name)
		return end_pos

	def info_attribute(self):
		print(f"position: [{self.pos_num}:{self.end_pos_num}] Number {self.num_cod} [{self.num}]")
		print(f"position: [{self.pos_let}:{self.end_pos_let}] Letter {self.let_cod} [{self.let}]")
		print(f"position: [{self.pos_cur}] Cursor")
		print(f'[{self.prefix}][{self.left}][{self.X}][{self.mid}][{self.Y}][{self.right}][{self.prefix}]: {self.info}')


	def update_position_number(self, value):
		self.position_number = value
		print(f"Update position number {value}")

	def update_number(self, start_number, padding_number, number):
		self.start_number = start_number
		self.padding_number = padding_number
		self.number = number

		print(f'New number: {self.number}, start: {self.start_number}, padding: {self.padding_number}')

	def on_click_number_mode_button(self, state):
		self.NumberWidget.set_state_from_number_mode(state)
		self.mode_number = state
		self.num = self.handle_number()

		self.X, self.mid, self.Y = self.handle_X_mid_Y()
		# print(f"Numeric Mode: {'checked' if state else 'unchecked'}: '{self.num}'")
		self.info = f"Numeric Mode: {'checked' if state else 'unchecked'}: '{self.num}'"
		self.info_attribute()

	def handle_left_right(self):
		left = self.text[len(self.prefix):self.pos_X]
		right = self.text[self.end_pos_Y:len(self.text) - len(self.suffix)]
		return left, right


	def handle_X_mid_Y(self):

		if self.num and self.let:
			if self.pos_num < self.pos_let:
				X, self.pos_X, self.end_pos_X, self.num_cod = self.num, self.pos_num, self.end_pos_num, "X"
				Y, self.pos_Y, self.end_pos_Y, self.let_cod = self.let, self.pos_let, self.end_pos_let, "Y"
			elif self.pos_num > self.pos_let:
				X, self.pos_X, self.end_pos_X, self.let_cod = self.let, self.pos_let, self.end_pos_let, "X"
				Y, self.pos_Y, self.end_pos_Y, self.num_cod = self.num, self.pos_num, self.end_pos_num, "Y"

			if end_pos_X == pos_Y:
				mid = ""
			else:
				mid = self.text[end_pos_X:pos_Y]
		else:
			if self.num:
				X, self.pos_X, self.end_pos_X, self.num_cod = self.num, self.pos_num, self.end_pos_num, "XY"
				self.let_cod = "None"
				self.pos_let = self.end_pos_X
				self.end_pos_let = self.end_pos_X
			elif self.let:
				X, self.pos_X, self.end_pos_X, self.let_cod = self.let, self.pos_let, self.end_pos_let, "XY"
				self.num_cod = "None"
				self.pos_num = self.end_pos_X
				self.end_pos_num = self.end_pos_X
			else:
				X, self.pos_X, self.end_pos_X, self.num_cod = "", 0, 0, "None"
				self.let_cod = "None"

			Y, self.pos_Y, self.end_pos_Y = "", self.end_pos_X, self.end_pos_X
			mid = ""

		return X, Y, mid

	def handle_number(self):
		"""Procesing number"""
		if self.mode_number:
			number = ("0" * (self.padding_num - len(str(self.start_num)))) + str(self.start_num)
		else:
			number = ""
			self.pos_num = 0
			self.end_pos_num = 0
		return number

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

	def update_pos_num_let(self):

		if self.num_cod == "XY":
			self.end_pos_X = self.get_end_pos(self.pos_X, self.X)
			self.pos_num = self.pos_X
			self.end_pos_num = self.get_end_pos(self.pos_num, self.num)
			self.pos_let = self.end_pos_num
			self.end_pos_let = self.get_end_pos(self.pos_let, self.let)
			self.pos_Y = self.get_end_pos(self.end_pos_X, self.Y)
			self.end_pos_Y = self.get_end_pos(self.pos_Y, self.Y)


	def handle_text(self, text):
		if self.text and len(text) > len(self.prefix) + len(self.X) + len(self.Y) + len(self.prefix):
			prefix = text[ : len(self.prefix)]
			left   = text[len(prefix) : self.pos_X]
			X      = text[self.pos_X : self.end_pos_X]
			mid    = text[self.end_pos_X : self.pos_Y]
			Y      = text[self.pos_Y : self.end_pos_Y]
			right  = text[self.end_pos_Y : len(text) - len(self.suffix)]
			suffix = text[len(text) - len(self.suffix): ]

			print(f"[{prefix}][{left}][{X}][{mid}][{Y}][{right}][{suffix}]:  ___HANDLE_TEXT___[{text}]")
		else:

			prefix, left, X, mid, Y, right, suffix = self.prefix, self.left, self.X, self.mid, self.Y, self.right, self.suffix
			print(f"[{prefix}][{text}][{X}][{mid}][{Y}][{right}][{suffix}]:  ___HANDLE_TEXT_else__{text}")

		return prefix, left, X, mid, Y, right, suffix
	def handle_add_part_X(self, prefix,text,items_diff, pos_cur):
		if pos_cur <= self.pos_X: #   >|[X] left side
			info_part = (f"[[pos_cur]{pos_cur}<={self.pos_X}[pos_X]], change___HERE___[LEFT]")
			self.pos_X = self.pos_X + items_diff
			self.left = text[len(prefix): self.pos_X]
			self.update_pos_num_let()
		elif pos_cur > self.pos_X: # [[X:] >| [:X]] >| [X] >| right side
			info_part = (f"[[pos_cur]{pos_cur}>{self.pos_X}[pos_X]] change___HERE___[RIGHT]")
			temptext = text[pos_cur:pos_cur + items_diff]
			self.right = temptext + self.right
			items_diff += items_diff

		return items_diff, info_part

	def handle_add_part_left(self,prefix, text, items_diff, pos_cur):
		self.pos_X = self.pos_X + items_diff
		self.left = text[len(prefix): self.pos_X]
		self.update_pos_num_let()
		info_part = (f"[[pos_cur]{pos_cur}<{self.pos_X}[pos_X]] change___HERE___[LEFT]")

		return items_diff, info_part

	def handle_add_part_right(self, prefix,text,items_diff, pos_cur):
		self.right = text[self.pos_Y: len(text) - len(self.suffix)]
		info_part = (f"[[pos_cur]{pos_cur}>{self.end_pos_Y}[end_pos_Y]] change___HERE___[RIGHT]")
		return items_diff, info_part


	def handle_addition(self, prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur):
		part = ""
		info_part = ""

		if prefix != self.prefix:
			part = "prefix"
		elif left != self.left:
			part = "left"
			items_diff, info_part = self.handle_add_part_left(prefix, text, items_diff, pos_cur)
		elif X != self.X:
			part = "X"
			items_diff, info_part = self.handle_add_part_X(prefix,text,items_diff, pos_cur)
		elif mid != self.mid:
			part = "mid"
		elif Y != self.Y:
			part = "Y"
		elif right != self.right:
			part = "right"
			items_diff, info_part = self.handle_add_part_right(prefix,text,items_diff, pos_cur)
		elif suffix != self.suffix:
			part = "suffix"

		self.info = f"___FIND_ADDITION___[{part}], {info_part}"

		self.maxR = len(self.prefix) + len(self.left) + len(self.mid) + len(self.right)
		self.minR = len(self.prefix)

		new_cur = self.pos_cur + items_diff
		newText = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix
		return newText, new_cur

	def handle_del_part_left(self, text, prefix, left , items_diff, pos_cur):

		in_left_old = self.text[len(prefix):pos_cur]
		in_left_new = text[len(prefix):pos_cur]

		if in_left_old == in_left_new: # [[]|>|[here]]

			info_part = (f"[[in_left_old]{in_left_old}=={in_left_new}[in_left_new]], change___HERE___[LEFT]--> [[][here]]")
			self.pos_X = self.pos_X + items_diff
			self.left = text[len(prefix):self.pos_X]
			self.update_pos_num_let()
			items_diff=0

		else: # [[here]|<|[]]
			info_part = (f"[[in_left_old]{in_left_old}!={in_left_new}[in_left_new]], change___HERE___[LEFT]--> [[here][]]")
			self.pos_X = self.pos_X + items_diff
			self.left = text[len(prefix):self.pos_X]
			self.update_pos_num_let()

		return items_diff, info_part

	def handle_del_part_right(self,text, prefix, left, right, items_diff, pos_cur):

		in_left_old = self.right[:pos_cur - self.end_pos_Y]
		in_left_new = right[:pos_cur - self.end_pos_Y]

		if in_left_old == in_left_new:  # [[]|>|[here]]

			info_part = (f"[[in_left_old]{in_left_old}=={in_left_new}[in_left_new]], change___HERE___[RIGHT]--> [[][here]]")

			items_diff = 0

		else:  # [[here]|<|[]]
			info_part = (f"[[in_left_old]{in_left_old}!={in_left_new}[in_left_new]], change___HERE___[RIGHT]--> [[here][]]")

		self.right = right


		return items_diff, info_part


	def handle_del_part_X(self, prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur):

		if pos_cur in range(self.pos_X, self.end_pos_X ):# left side >|[X]
			if self.mid:
				print("TODO : MID ")
				info_part = (f"[[pos_cur]{pos_cur}<={self.pos_X}[pos_X]], change___HERE___[MID]")
			elif self.right:
				info_part = (f"[[pos_cur]{pos_cur} in {range(self.pos_X, self.end_pos_X)}[pos_X]],, change___HERE___[RIGHT]")
				self.right = right
				items_diff = 0
			else:
				info_part = (f"[[pos_cur]{pos_cur} in {range(self.pos_X, self.end_pos_X)}[pos_X]], change___HERE___[X]")
				items_diff = 0

			self.update_pos_num_let()

		elif pos_cur == self.end_pos_X: # [X]|< right side
			if left:
				info_part = (f"[[pos_cur]{pos_cur}>{self.end_pos_X}[end_pos_X]] change___HERE___[LEFT]")
				self.pos_X = self.pos_X + items_diff
				self.left = text[len(prefix): self.pos_X]
				self.update_pos_num_let()
			else: # [left = false][X]|<|
				info_part = (f"[[pos_cur]{pos_cur}>{self.end_pos_X}[end_pos_X]] change___HERE___[LEFT NONE] RUTERN NAME")
				items_diff = 0

		return items_diff, info_part



	def handle_deletion(self, prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur):
		part = ""
		info_part = ""

		if prefix != self.prefix:
			part = "prefix"
		elif left != self.left:
			part = "left"
			items_diff, info_part = self.handle_del_part_left(text, prefix, left , items_diff, pos_cur)
		elif X != self.X:
			part = "X"
			items_diff, info_part = self.handle_del_part_X(prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur)
		elif mid != self.mid:
			part = "mid"
		elif Y != self.Y:
			part = "Y"
		elif right != self.right:
			part = "right"
			items_diff, info_part = self.handle_del_part_right(text, prefix, left, right, items_diff, pos_cur)
		elif suffix != self.suffix:
			part = "suffix"

		self.info = f"___FIX_deletion___ --> {part}, {info_part}"

		self.maxR = len(self.prefix) + len(self.left) + len(self.mid) + len(self.right)
		self.minR = len(self.prefix)

		new_cur = self.pos_cur + items_diff
		newText = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix
		return newText, new_cur


	def do_text_edited(self, text):

		newText    = ""
		pos_cur    = self.pos_cur
		new_cur     = 0
		items_diff = len(text) - len(self.text)
		prefix, left, X, mid, Y, right, suffix = self.handle_text(text)

		if self.text and len(text) > len(self.prefix)+ len(self.X) + len(self.Y) + len(self.prefix):
			if items_diff > 0:  # Added items
				newText, new_cur = self.handle_addition(prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur)
			elif items_diff < 0:  # Removed items
				newText, new_cur = self.handle_deletion(prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur)

		else:
			if len(text) == len(self.prefix) + len(self.X) + len(self.Y) + len(self.suffix) or len(text) == 0:

				newText = ""
				self.maxR = 0
				self.pos_X = 0
				self.left = ""
				self.right = ""
				self.update_pos_num_let()
				self.info = f" ____REMOVE____ --> [prefix][number][letter][suffix]"
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setClearButtonEnabled(False)

			else:

				self.maxR = len(text) + len(self.prefix)
				self.pos_X = len(text) + len(self.prefix)
				self.left = text

				newText = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix
				new_cur = self.pos_X
				self.update_pos_num_let()
				self.info = " ___ADD___ --> [prefix][number][letter][suffix]"
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setClearButtonEnabled(True)



		self.text = newText

		self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(newText)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(new_cur)

		self.NumberWidget.index_slider.setRange(self.minR, self.maxR)
		self.NumberWidget.index_SpinBox.setRange(self.minR, self.maxR)
		self.NumberWidget.index_slider.setValue(self.pos_X)
		self.NumberWidget.index_SpinBox.setValue(self.pos_X)


		self.info_attribute()



		# print(f"textEdited '{text}',prefix '{self.prefix}',suffix '{self.suffix}', number '{self.number}', oldTextLine '{self.old_Text}'")
		# Delete_number = ""
		# old_text = self.old_Text
		# start = self.position_number
		# cursor_pos = self.cursor_pos
		#
		#
		# left_text = text[:self.position_number] # чекнуть эти атрибуты нужны они для инициализации каждый раз когда запускаем фенкции
		# right_text = text[self.end_position_number:]  # чекнуть эти атрибуты нужны они для инициализации каждый раз когда запускаем фенкции
		# sectionText = text[self.position_number:self.end_position_number]
		#
		# items_add = len(text) - len(self.old_Text)
		# items_removed = len(self.old_Text) - len(text)
		#
		# self.maxRange = len(text) - len(self.number) - len(self.suffix)
		# self.minRange = len(self.prefix)
		#
		# right_without_suffix = self.old_Text[self.end_position_number:len(self.old_Text) - len(self.suffix)]
		#
		# if len(text) > len(self.number) + len(self.prefix) + len(self.suffix) and self.old_Text:
		# 	if len(text) > len(self.old_Text):  # items_add
		# 		self.old_Text = text
		#
		# 		if sectionText != self.number or self.number == "" and cursor_pos <= self.position_number:  # items_add in left_text! [left_text] >|< (sectionText != [Number]) [right_text]
		# 			self.position_number += items_add
		# 			left_text, right_text, sectionText = self.update_positions_for_text(text, "1")
		#
		# 		else:
		# 			pass  # items_add in right_text! [left_text] [Number] >|< [right_text]
		#
		#
		# 	elif len(text) < len(self.old_Text):  # items_removed
		# 		self.old_Text = text
		# 		if sectionText != self.number or self.number == "" and cursor_pos < self.position_number:  # items_removed in left_text! [left_text] >|< (sectionText != [Number]) [right_text]
		# 			self.position_number -= items_removed
		# 			left_text, right_text, sectionText = self.update_positions_for_text(text, "2")
		#
		# 			if self.position_number <len(self.prefix) and len(self.prefix) != cursor_pos:  # start cannot to be negative  |  [-1][number]|[right_text]
		#
		# 				left_text, right_text, sectionText =  self.handle_start_below_minimum(old_text, "3")
		# 				Delete_number = "Delete number, left negative"
		#
		# 			elif self.prefix != text[:len(self.prefix)]:
		#
		# 				left_text, right_text, sectionText = self.handle_prefix_deletion(old_text, items_removed, "4")
		# 				Delete_number = "Delete prefix, left negative -> prefix "
		#
		# 			elif right_without_suffix == "" and sectionText != self.number and self.position_number + 1 == cursor_pos:  # end cannot to be negative  |  [number]|[][_suffix]
		#
		# 				left_text, right_text, sectionText = self.handle_right_negative(old_text, items_removed, cursor_pos, "5")
		# 				Delete_number = "Delete number, right negative"
		#
		# 			if sectionText != self.number:  # [Text]DEL====>[Number]<===DEL[Text] Delet Number!
		# 				print("CHeck ", self.position_number, cursor_pos)
		# 				left_text, right_text, sectionText = self.handle_section_text_change(old_text, items_removed, cursor_pos, "6")
		#
		# 				# Delete_number = "Delete number , right"
		# 				Delete_number = "Delete number, left or right"
		#
		# 				# self.position_number += items_removed
		# 				# start = self.position_number
		# 				# end = start + len(self.number)
		#
		# 				# if start == cursor_pos:  # [Text]>>DEL>>|[Number][(T)ext] Delet Number!
		# 				#
		# 				# 	Delete_number = "Delete number , right"
		# 				# 	left_text = old_text[:start]
		# 				# 	right_text = old_text[end + items_removed:]
		# 				# 	NewText = left_text + self.number + right_text
		# 				#
		# 				# 	self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(NewText)
		# 				# 	self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(start)
		# 				# 	self.old_Text = NewText
		# 				#
		# 				# 	if right_text == "":
		# 				# 		self.maxRange = len(NewText) - len(self.number)
		# 				#
		# 				# else:  # self.End_index_number <= self.cursor_pos: # [Tex(t)][Number]|<<<DEL<<<[Text] Delet Number!
		# 				#
		# 				# 	self.position_number -= items_removed
		# 				# 	Delete_number = "Delete number, left"
		# 				#
		# 				# 	left_text = old_text[:start - items_removed]
		# 				# 	right_text = old_text[end:]
		# 				# 	NewText = left_text + self.number + right_text
		# 				#
		# 				# 	start = self.position_number
		# 				# 	end = start + len(self.number)
		# 				#
		# 				# 	self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(NewText)
		# 				# 	self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(end)
		# 				# 	self.old_Text = NewText
		#
		# 			else:
		#
		# 				if self.position_number <= 0 + len(self.prefix):  # start cannot be negative  |  [-1][number]|[right_text]
		# 					self.position_number = 0 + len(self.prefix)
		# 					self.old_Text = old_text
		# 				elif cursor_pos == len(self.prefix) and self.prefix != text[:len(self.prefix)]:
		#
		# 					self.old_Text = old_text
		#
		# 				elif right_without_suffix == "Delete number, right negative":
		# 					self.old_Text = old_text
		#
		# 				else:
		# 					self.old_Text = text
		#
		# 		elif self.suffix != text[len(text) - len(self.suffix):]:
		#
		# 			Delete_number = "Delete suffix, right negative"
		#
		# 			self.maxRange = len(old_text) - len(self.number) - len(self.suffix)
		#
		# 			self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(old_text)
		# 			self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(cursor_pos)
		#
		# 			self.old_Text = old_text
		#
		# else:
		#
		# 	if len(text) == len(self.number) + len(self.prefix) + len(self.suffix) or len(text) == 0:
		#
		# 		self.RenameWidget.LineEditor.AutoComplete_line_edit.setText("")
		# 		self.old_Text = ""
		# 		left_text = ""
		# 		right_text = ""
		# 		self.number = ""
		# 		self.maxRange = 0
		# 		Delete_number = "removed Number"
		# 		self.position_number = 0
		#
		# 	else:
		#
		# 		self.maxRange = len(text) + len(self.prefix)
		# 		self.position_number = len(text) + len(self.prefix)
		# 		start = self.position_number
		# 		Delete_number = "add Number"
		# 		left_text = self.prefix + text
		# 		right_text = "" + self.suffix
		#
		# 		NewText = self.prefix + text + self.number + self.suffix
		#
		# 		self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(NewText)
		# 		self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(start)
		#
		# 		self.old_Text = NewText
		#
		# left_text = left_text[len(self.prefix):]
		# right_text = right_text[:len(right_text) - len(self.suffix)]
		#
		# print("[{3}][{0}][{2}][{1}][{4}] Range = {5} {6}".format(left_text, right_text, self.number, self.prefix, self.suffix, self.maxRange,Delete_number))
		#
		# self.NumberWidget.index_slider.setRange(self.minRange, self.maxRange)
		# self.NumberWidget.index_SpinBox.setRange(self.NumberWidget.index_slider.minimum(), self.NumberWidget.index_slider.maximum())
		# self.NumberWidget.index_slider.setValue(self.position_number)
		# self.NumberWidget.index_SpinBox.setValue(self.position_number)
		#
		# self.number = self.handle_number()

	def posNumber_cursor(self, oldPos, newPos):
		self.pos_cur = newPos

		# MineDataName = self.RenameWidget.LineEditor.AutoComplete_line_edit.oldMineData
		# name = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()

		# print(newPos, "cursor newPos")
		# if name != MineDataName:
		# 	# self.prefix, self.suffix = self.handle_prefix_suffix()
		#
		# 	prefix = self.prefix
		# 	suffix = self.suffix
		# 	Number = self.number
		# 	self.cursor_pos = newPos
		#
		# 	start = self.position_number
		# 	end = start + len(Number)
		#
		# 	if MineDataName:
		# 		print(MineDataName)
		# 		if MineDataName in name:
		# 			print(name)
		# 			SplitName = name.split(MineDataName)
		# 			name = SplitName[0] + SplitName[1]
		#
		# 	if newPos in range(start + 1, end):
		# 		if oldPos >= end:
		#
		# 			self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(start)
		#
		# 		elif oldPos <= self.position_number:
		#
		# 			self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(end)
		# 		print("number")
		#
		# 	if prefix:
		# 		if newPos in range(0, len(prefix)):
		# 			self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(len(prefix))
		# 			print("prefix")
		#
		# 	if suffix:
		#
		# 		no_suffix = len(name) - len(suffix)
		#
		# 		if newPos in range(no_suffix + 1, len(name)) or newPos >= len(name):
		# 			self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(no_suffix)
		# 			print("suffix")