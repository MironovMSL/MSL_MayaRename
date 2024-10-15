from asyncio import current_task

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
		self.resources   = Resources.get_instance()
		self.QSettings   = QtCore.QSettings(self.resources.config_path, QtCore.QSettings.IniFormat)
		self.FixedHeigt  = 200
		# mode----------------------------
		self.mode_button = None # mode button for button and lineEdits
		self.mode_number = None # mode number for Numeric
		self.mode_letter = None # mode letter for letter in leneEdite
		# blocks text------------------------------------
		self.prefix      = None  # [prefix]
		self.left        = None  # [left_text]
		self.mid         = None  # [mid_text]
		self.right       = None  # [right text]
		self.suffix      = None  # [suffix]

		self.X           = None  # [X] number or letter
		self.pos_X       = None  # [X] position [pos:end]
		self.end_pos_X   = None  # [X] end position [pos:end]

		self.Y           = None  # [Y] number or letter
		self.pos_Y       = None  # [Y] position [pos:end]
		self.end_pos_Y   = None  # [Y] end position [pos:end]

		self.text        = None  # old text for comperisen [last Text]
		# number-----------------------------------
		self.num         = None  # number start = 1, padding = 2, number = [01]
		self.pos_num     = None  # position number in slider
		self.num_cod     = None  # num cod X or Y
		# letter----------------------------------
		self.let         = None  # letter  ~ [lettter]
		self.pos_let     = None  # position letter [pos:end]
		self.let_cod     = None  # let cod X or Y
		# Range and cursor-------------------------------
		self.pos_cur     = None  # cursor position for comparison
		self.maxR        = None  # maximum range for position [number] and [letter]
		self.minR        = None  # minimum range for position [number] and [letter]

		# Setting ------------------------
		self.setFixedHeight(self.FixedHeigt)
		# Run function ------------------------
		self.create_Widgets()
		self.create_layouts()
		self.create_connections()
		self.init_attribute()
		self.info_attribute()

	def create_Widgets(self):

		self.FunctionWidget      = FunctionWidget()
		self.LabelWidget         = LabelWidget()
		self.RenameButton        = QtWidgets.QPushButton("Rename")
		self.RenameButton.setFixedSize(50, 75)
		self.RenameWidget        = RenameWidget()
		self.NumberWidget        = NumberWidget()
		self.LetterWidget        = LetterWidget()
		self.SuffixPrefixWidget  = SuffixPrefixWidget()
		self.QuickListButtonName = QuickListButtonName()
		self.CasheNameWidget     = CasheNameWidget()

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
		self.LabelWidget.button_mode.changeStateButtonMode.connect(self.on_click_button_mode_button)
		self.LetterWidget.itEditLetter.connect(self.on_click_letter_mode)

		self.RenameWidget.LineEditor.AutoComplete_line_edit.textEdited.connect(self.do_text_edited)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.itDropName.connect(self.drop_text)
		self.NumberWidget.new_number_Signal.connect(self.update_number)
		self.NumberWidget.new_position_Signal.connect(self.update_position_number)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.cursorPositionChanged.connect(self.posNumber_cursor)
		self.SuffixPrefixWidget.itEditPrefix.connect(self.update_prefix)
		self.SuffixPrefixWidget.itEditSuffix.connect(self.update_suffix)

	def init_attribute(self):

		# mode----------------------------
		self.mode_button = self.QSettings.value("startup/mode_button", False, bool)  # mode number for button and lineEdits
		self.mode_number = self.QSettings.value("startup/mode_number", False, bool)  # mode number for Numeric
		self.mode_letter = self.QSettings.value("startup/mode_letter", False, bool)
		# number-----------------------------------
		self.start_num   = self.QSettings.value("startup/start_number", 1, int)  # start number ~ 1
		self.padding_num = self.QSettings.value("startup/padding_number", 2, int)  # pading number ~ 2 = 00
		self.num         = self.handle_number()  # number start = 1, padding = 2, number = [01]
		self.pos_num     = self.QSettings.value("startup/position_number", 0, int)  # position number [pos:end]
		self.end_pos_num = self.pos_num + len(self.num)  # end position num [pos:end]
		self.num_cod     = ""
		# letter----------------------------------
		self.pos_let     = 0  # position letter [pos:end]
		self.end_pos_let = 0  # end position letter [pos:end]
		self.let         = self.QSettings.value("startup/letter", "", str)  # letter  ~ [lettter]
		self.let_cod     = ""
		# Range and cursor-------------------------------
		self.pos_cur     = 0  # cursor position for comparison
		self.maxR        = 0  # maximum range for position [number] and [letter]
		self.minR        = 0  # minimum range for position [number] and [letter]
		# blocks text------------------------------------
		self.text        = ""  # old text for comperisen [last Text]
		self.prefix, self.suffix  = self.handle_prefix_suffix()
		self.X, self.mid, self.Y  = self.handle_X_mid_Y()
		self.left ,self.right     = self.handle_left_right()
		#------------------------------



		self.info = "Initialization attribute"

	def get_end_pos(self, pos, name):
		end_pos = pos + len(name)
		return end_pos

	def info_attribute(self):
		print(f"position: [{self.pos_num}] Number {self.num_cod} [{self.num}],")
		print(f"position: [{self.pos_let}] Letter {self.let_cod} [{self.let}]")
		print(f"position: [{self.pos_X}:{self.end_pos_X}] X [{self.X}],")
		print(f"position: [{self.pos_Y}:{self.end_pos_Y},{len(self.X)}] Y [{self.Y}],")
		print(f"position: [{self.pos_cur}] Cursor")
		print(f'[{self.prefix}][{self.left}][{self.X}][{self.mid}][{self.Y}][{self.right}][{self.suffix}]: {self.info}')



	def drop_text(self, text, pos_cur):
		self.pos_cur = pos_cur
		self.do_text_edited(text)


	def on_click_letter_mode(self, letter, state):

		self.mode_letter = state

		pos_cur = self.pos_cur
		text    = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()
		new_cur = 0
		newText = ""

		print(letter, state)

		if state:
			if text:
				if self.let_cod == "Y":
					self.Y = letter
					if pos_cur >= self.pos_Y:
						new_cur = pos_cur + len(letter)
					else:
						new_cur = self.pos_cur
				elif self.let_cod  == "X":
					self.X = letter
					if pos_cur >= self.pos_X:
						new_cur = pos_cur + len(letter)
			else:
				if self.let_cod == "Y":
					self.Y = letter
					new_cur = cur_pos
				elif self.let_cod  == "X":
					self.X = letter
					new_cur = self.pos_cur

			newText = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.prefix

		else:

			if text:
				if self.let_cod == "Y":

					if pos_cur > self.end_pos_Y:
						new_cur = pos_cur - len(self.Y)
					else:
						new_cur = self.pos_cur

					self.Y = ""

				elif self.let_cod == "X":

					if pos_cur > self.pos_X:
						new_cur = pos_cur - len(self.X)

					self.X = ""
			else:
				new_cur = self.pos_cur
				if self.let_cod == "Y":
					self.Y = ""

				elif self.let_cod == "X":
					self.X = ""

			newText = ""

		self.mode_letter = state
		self.info = f"Letter Mode: {'checked' if state else 'unchecked'}: '{self.let}'"
		self.update_ui_elements(newText, new_cur)



	def on_click_number_mode_button(self, state):
		self.NumberWidget.set_state_from_number_mode(state)
		self.state_number(state)

	def state_number(self, state):

		dift             = len(self.num)

		self.mode_number = state
		self.num         = self.handle_number()
		self.end_pos_num = self.pos_num + dift

		pos_cur = self.pos_cur
		text    = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()
		new_cur = 0
		newText = ""

		if state:
			if text:
				if self.num_cod == "X":
					self.X = self.num

					if pos_cur >= self.pos_X:  # [X]>|
						new_cur = pos_cur + len(self.X)
					else:
						new_cur = pos_cur

					self.update_pos_X_Y_num_let(side="Y", len_X=len(self.num))

				elif self.num_cod == "Y":
					self.Y = self.num

					if pos_cur >= self.pos_Y:  # [Y]>|
						new_cur = pos_cur + len(self.Y)
				else:

					new_cur = cur_pos

				newText = self.get_new_text()

			else:
				if self.num_cod == "X":
					self.X = self.num

				elif self.num_cod == "Y":
					self.Y = self.num



		else:
			if text:
				if self.num_cod == "X":
					self.X = self.num
					if pos_cur > self.pos_num:  # [X]>|
						new_cur = pos_cur - dift
					else:
						new_cur = pos_cur

					self.update_pos_X_Y_num_let(side="Y", len_X=-dift)

				elif self.num_cod == "Y":
					self.Y = self.num

					if pos_cur >= self.pos_Y:  # [Y]>|
						new_cur = pos_cur - dift
			else:
				if self.num_cod == "X":
					self.X = self.num

				elif self.num_cod == "Y":
					self.Y = self.num

			newText = self.get_new_text()

		self.info = f"Numeric Mode: {'checked' if state else 'unchecked'}: '{self.num}'"
		self.update_ui_elements(newText, new_cur)

	def update_prefix(self, prefix):
		text = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()

		if self.mode_button:
			if text:

				item_dift   = len(prefix) - len(self.prefix) # prefix - prefix_ = -1
				self.prefix = prefix

				newText = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix
				new_cur = self.pos_cur + item_dift
				self.pos_X += item_dift
				self.update_pos_num_let()
				self.update_range()



				self.update_ui_elements(newText, new_cur)
				self.info = (f'Button mode "{self.mode_button}", New prefix: [{self.prefix}]')
			else:
				self.prefix = prefix

			self.info = (f'Button mode "{self.mode_button}", New prefix: [{self.prefix}]')

		else:
			self.info = (f'Button mode "{self.mode_button}", Initialization prefix: [{prefix}]')


		self.info_attribute()


	def update_suffix(self, suffix):
		text = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()


		if self.mode_button:
			self.suffix = suffix
			if text:

				newText = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix
				new_cur = self.pos_cur


				self.update_ui_elements(newText, new_cur)

			self.info = (f'New suffix: [{self.suffix}]')

		else:
			self.info = (f'Button mode {self.mode_button}, Initialization suffix: [{suffix}]')

		self.info_attribute()


	def on_click_button_mode_button(self, state):
		self.state_prefix_suffix(state)


	def state_prefix_suffix(self, state):
		self.mode_button         = state
		self.prefix, self.suffix = self.handle_prefix_suffix()

		prefix = self.SuffixPrefixWidget.prefix_Editline.AutoComplete_line_edit.text()

		pos_cur                  = self.pos_cur
		new_cur                  = 0
		text                     = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()
		newText                  = ""

		if state:
			if text:
				self.pos_X += len(prefix)
				self.maxR  += len(prefix)
				self.minR   = len(prefix)

				new_cur     = self.pos_cur + len(self.prefix)
				self.update_pos_num_let()

				newText = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix

		else:
			if text:
				if pos_cur < len(prefix):
					new_cur = 0
				else:
					new_cur = pos_cur - len(prefix)

				self.pos_X -= len(prefix)
				self.maxR  -= len(prefix)
				self.minR   = 0
				new_cur     = pos_cur - len(prefix)
				self.update_pos_num_let()

				newText = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix

			else:
				newText = ""
				new_cur = 0


		self.info = f"Button Mode: {'checked' if state else 'unchecked'}: [{self.prefix}] [ ] [{self.suffix}]"
		self.update_ui_elements(newText, new_cur)


	def update_position_number(self, value):

		value_slider         = self.NumberWidget.pos_num_slider.value()
		self.NumberWidget.pos_num_slider.setValue(value)
		self.pos_num         = value
		print(f"Update position number {value}, {value_slider}={value}")
		pos_cur              = self.pos_cur

		if value_slider != value:
			self.info = (f"Update position number {value}, {value_slider}!={value}")
			if self.num_cod == "XY":

				text       = self.prefix + self.left + self.right + self.suffix
				self.left  =  text[ len(self.prefix) : value ]
				self.right = text[ value : len(text) - len(self.suffix) ]
				self.pos_X = value

				self.update_pos_num_let()

				self.text = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix

				self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(self.text)
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(pos_cur)
			self.info_attribute()

		print(self.pos_let, self.pos_Y)


	def update_number(self, start_number, padding_number, number):
		self.start_num           = start_number
		self.padding_num         = padding_number
		self.num                 = number
		self.end_pos_num         = self.pos_num + len(self.num)
		self.X, self.mid, self.Y = self.handle_X_mid_Y()
		text                     = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()

		self.update_range()
		self.update_pos_num_let()

		if text:
			if self.pos_cur <= self.pos_num:
				new_cur = self.pos_cur
			else:
				new_cur = self.pos_cur + self.padding_num

			newText = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix

		else:
			newText = ""
			new_cur = self.pos_cur

		self.info = (f'New number: {self.num}, start: {self.start_num}, padding: {self.padding_num}')
		self.update_ui_elements(newText, new_cur)


	def update_range(self):
		self.maxR = len(self.prefix) + len(self.left) + len(self.mid) + len(self.right)
		self.minR = len(self.prefix)

	def handle_left_right(self):
		left = self.text[len(self.prefix):self.pos_X]
		right = self.text[self.end_pos_Y:len(self.text) - len(self.suffix)]
		return left, right

	def handle_X_mid_Y(self):

		# if self.num and self.let:
		# 	if self.pos_num < self.pos_let:
		# 		X, self.pos_X, self.end_pos_X, self.num_cod = self.num, self.pos_num, self.end_pos_num, "X"
		# 		Y, self.pos_Y, self.end_pos_Y, self.let_cod = self.let, self.pos_let, self.end_pos_let, "Y"
		# 	elif self.pos_num > self.pos_let:
		# 		X, self.pos_X, self.end_pos_X, self.let_cod = self.let, self.pos_let, self.end_pos_let, "X"
		# 		Y, self.pos_Y, self.end_pos_Y, self.num_cod = self.num, self.pos_num, self.end_pos_num, "Y"
		#
		# 	if end_pos_X == pos_Y:
		# 		mid = ""
		# 	else:
		# 		mid = self.text[end_pos_X:pos_Y]
		# # else:
		# 	if self.num:
		# 		X, self.pos_X, self.end_pos_X, self.num_cod = self.num, self.pos_num, self.end_pos_num, "XY"
		# 		self.let_cod = "None let"
		# 		self.pos_let = self.end_pos_X
		# 		self.end_pos_let = self.end_pos_X
		# 	elif self.let:
		# 		X, self.pos_X, self.end_pos_X, self.let_cod = self.let, self.pos_let, self.end_pos_let, "XY"
		# 		self.num_cod = "None num"
		# 		self.pos_num = self.end_pos_X
		# 		self.end_pos_num = self.end_pos_X
		# 	else:
		# 		X, self.pos_X, self.end_pos_X, self.num_cod = self.num, self.pos_num, self.end_pos_num, "None num"
		# 		self.let_cod = "None let"
		#
		# 	Y, self.pos_Y, self.end_pos_Y = "", self.end_pos_X, self.end_pos_X
		# 	mid = ""

			#============================================
		pos_dift = 0

		if self.pos_num < self.pos_let:

			X, self.num_cod = self.num, "X"
			self.pos_X      = self.pos_num
			self.end_pos_X  = self.pos_X + len(X)

			Y, self.let_cod = self.let, "Y"
			self.pos_Y      = self.pos_let + len(X)
			self.end_pos_Y  = self.pos_Y + len(Y)

		elif self.pos_num > self.pos_let:

			X, self.let_cod = self.let,"X"
			self.pos_X      = self.pos_let
			self.end_pos_X  = self.pos_X + len(X)

			Y, self.num_cod = self.num, "Y"
			self.pos_Y      = self.pos_num + len(X)
			self.end_pos_Y  = self.pos_Y + len(Y)

		elif self.pos_num == self.pos_let:
			if not self.num_cod:
				print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
				X, self.num_cod = self.num, "X"
				self.pos_X = self.pos_num
				self.end_pos_X = self.pos_X + len(X)

				Y, self.let_cod = self.let, "Y"
				self.pos_Y = self.pos_let + len(X)
				self.end_pos_Y = self.pos_Y + len(Y)

			elif self.num_cod == "X":

				X, self.num_cod = self.num, "X"
				self.pos_X = self.pos_num
				self.end_pos_X = self.pos_X + len(X)

				Y, self.let_cod = self.let, "Y"
				self.pos_Y = self.pos_let + len(X)
				self.end_pos_Y = self.pos_Y + len(Y)

			elif self.let_cod == "X":

				X, self.let_cod = self.let, "X"
				self.pos_X = self.pos_let
				self.end_pos_X = self.pos_X + len(X)

				Y, self.num_cod = self.num, "Y"
				self.pos_Y = self.pos_num + len(X)
				self.end_pos_Y = self.pos_Y + len(Y)


		mid = self.text[self.end_pos_X:self.pos_Y]
		print(self.let_cod)

		return X, Y, mid

	def handle_number(self):
		"""Procesing number"""
		if self.mode_number:
			number = ("0" * (self.padding_num - len(str(self.start_num)))) + str(self.start_num)
		else:
			number = ""
			self.update_pos_num_let()
		return number

	def handle_prefix_suffix(self):
		"""Prefix and Suffix Processing"""
		if self.mode_button:

			prefix = self.SuffixPrefixWidget.prefix_Editline.AutoComplete_line_edit.text()
			suffix = self.SuffixPrefixWidget.suffix_Editline.AutoComplete_line_edit.text()
			print(prefix,suffix)
		else:
			prefix = ""
			suffix = ""
		return prefix, suffix

	def update_pos_num_let(self):
		# DELET function
		if self.num_cod == "X":

			self.pos_num     = self.pos_X

			self.end_pos_X   = self.get_end_pos(self.pos_X, self.X)

			self.pos_let     = self.end_pos_num
			self.end_pos_let = self.get_end_pos(self.pos_let, self.let)

			self.pos_Y       = self.get_end_pos(self.end_pos_X, self.Y)
			self.end_pos_Y   = self.get_end_pos(self.pos_Y, self.Y)

		elif self.let_cod == "X" :

			self.pos_num     = self.pos_X
			self.end_pos_num = self.get_end_pos(self.pos_num, self.num)

			self.end_pos_X   = self.get_end_pos(self.pos_X, self.X)

			self.pos_let     = self.end_pos_num
			self.end_pos_let = self.get_end_pos(self.pos_let, self.let)

			self.pos_Y       = self.get_end_pos(self.end_pos_X, self.Y)
			self.end_pos_Y   = self.get_end_pos(self.pos_Y, self.Y)
		#______________________________________________________

	def update_pos_X_Y_num_let(self, items_dift = 0, side="X", len_X = 0, reset = False):

		if reset:
			self.pos_X = 0
			self.end_pos_X = self.get_end_pos(self.pos_X, self.X)

			self.pos_Y = self.end_pos_X
			self.end_pos_Y = self.get_end_pos(self.pos_Y, self.Y)

			self.pos_num = 0
			self.pos_let = 0

		else:
			if side == "X":

				self.pos_X     = self.pos_X + items_dift
				self.end_pos_X = self.get_end_pos(self.pos_X, self.X)

				self.pos_Y     = self.pos_Y + items_dift
				self.end_pos_Y = self.get_end_pos(self.pos_Y, self.Y)

				self.pos_num  += items_dift
				self.pos_let  += items_dift

			elif side == "Y":

				self.end_pos_X = self.get_end_pos(self.pos_X, self.X)

				self.pos_Y = self.pos_Y + items_dift + len_X
				self.end_pos_Y = self.get_end_pos(self.pos_Y, self.Y)

				if self.num_cod == "Y":
					self.pos_num = self.pos_num + items_dift
				else:
					self.pos_let = self.pos_let + items_dift

	def handle_text(self, text):

		if self.text and len(text) > len(self.prefix) + len(self.X) + len(self.Y) + len(self.suffix):
			prefix = text[ : len(self.prefix) ]
			left   = text[ len(self.prefix) : self.pos_X ]
			X      = text[ self.pos_X : self.end_pos_X ]
			mid    = text[ self.end_pos_X : self.pos_Y ]
			Y      = text[ self.pos_Y : self.end_pos_Y ]
			right  = text[ self.end_pos_Y : len(text) - len(self.suffix) ]
			suffix = text[ len(text) - len(self.suffix): ]

			print(f"[{prefix}][{left}][{X}][{mid}][{Y}][{right}][{suffix}]:  ___HANDLE_TEXT___[{text}]")
		else:

			prefix, left, X, mid, Y, right, suffix = self.prefix, self.left, self.X, self.mid, self.Y, self.right, self.suffix
			print(f"[{prefix}][{text}][{X}][{mid}][{Y}][{right}][{suffix}]:  ___HANDLE_TEXT_else__{text}")

		return prefix, left, X, mid, Y, right, suffix



	def handle_add_part_left(self,prefix, text, items_diff, pos_cur):
		# self.pos_X = self.pos_X + items_diff
		# self.update_pos_num_let()
		# self.update_pos_X_and_Y(items_dift=items_dift)
		self.update_pos_X_Y_num_let(items_dift=items_diff, side="X")
		self.left = text[len(prefix): self.pos_X]
		info_part = (f"[[pos_cur]{pos_cur}<{self.pos_X}[pos_X]] change___HERE-->[LEFT]")

		return items_diff, info_part

	def handle_add_part_X(self, prefix,text,items_diff, pos_cur):
		if pos_cur <= self.pos_X: #   >|[X] left side

			info_part = (f"[[pos_cur]{pos_cur}<={self.pos_X}[pos_X]], change___HERE___[LEFT]")
			self.update_pos_X_Y_num_let(items_dift=items_diff, side="X")
			self.left = text[len(prefix): self.pos_X]

		elif pos_cur > self.pos_X: # [[X:] >| [:X]] >| [X] >| right side

			info_part = (f"[[pos_cur]{pos_cur}>{self.pos_X}[pos_X]] change___HERE___[MID]")
			self.update_pos_X_Y_num_let(items_dift=items_diff, side="Y")
			temptext = text[pos_cur:pos_cur + items_diff]
			self.mid = temptext + self.mid
			items_diff += items_diff

		return items_diff, info_part

	def handle_add_part_right(self, prefix,text,items_dift, pos_cur):
		if pos_cur <= self.pos_X: #[X]=[Y]
			info_part = (f"[[cur]{pos_cur}<={self.pos_X}[X]] change___HERE-->[LEFT]")
			self.update_pos_X_Y_num_let(items_dift=items_dift, side="X", len_X=0)
			# self.pos_X = self.pos_X + items_diff
			self.left = text[len(prefix): self.pos_X]
			# self.update_pos_num_let()

		else:
			info_part = (f"[[cur]{pos_cur}>{self.end_pos_Y}[end_Y]] change___HERE-->[RIGHT]")
			self.right = text[self.end_pos_Y: len(text) - len(self.suffix)]

		return items_dift, info_part

	def handle_add_part_mid(self, text, items_diff, pos_cur):

		self.update_pos_X_Y_num_let(items_dift=items_diff, side="Y")
		self.mid = text[self.end_pos_X: self.pos_Y]
		info_part = (f"[[pos_cur]{pos_cur}>{self.end_pos_X}[end_pos_X]] change___HERE-->[MID]")


	def handle_addition(self, prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur):
		part = ""
		info_part = ""
		#------------------------------
		print("------------------------------!!!!!!!!!!")

		# Вычисляем границы заранее для улучшения читаемости
		prefix_end = len(self.prefix)
		left_end = prefix_end + len(self.left)
		x_end = left_end + len(self.X)
		mid_end = x_end + len(self.mid)
		y_end = mid_end + len(self.Y)
		right_end = y_end + len(self.right)
		suffix_end = right_end + len(self.suffix)


		# Логика условий с self.text[:]
		if 0 <= pos_cur < prefix_end:
			part = "prefix"
			print("TODO: prefix", list(range(0, prefix_end)))

		elif prefix_end <= pos_cur <= left_end:
			part = "left"
			print("TODO: left", list(range(prefix_end, left_end)))

		elif left_end < pos_cur < x_end:
			part = "X"
			print("TODO: X", list(range(left_end, x_end)))

		elif x_end <= pos_cur <= mid_end:
			part = "mid"
			print("TODO: MID", list(range(x_end, mid_end)))

		elif mid_end < pos_cur < y_end:
			part = "Y"
			print("TODO: Y", list(range(mid_end, y_end)))

		elif y_end <= pos_cur <= right_end:
			part = "right"
			print("TODO: right", list(range(y_end, right_end)))

		elif right_end < pos_cur <= suffix_end:
			part = "suffix"
			print("TODO: suffix", list(range(right_end, suffix_end)))

		print("------------------------------!!!!!!!!!!")
		#------------------------------


		if prefix != self.prefix:
			part = "prefix"
		elif left != self.left:
			part = "left"
			items_diff, info_part = self.handle_add_part_left(prefix, text, items_diff, pos_cur)
		elif X != self.X:
			part = "X"
			items_diff, info_part = self.handle_add_part_X(prefix, text, items_diff, pos_cur)
		elif mid != self.mid:
			part = "mid"
		elif Y != self.Y:
			part = "Y"
		elif right != self.right:
			part = "right"
			items_diff, info_part = self.handle_add_part_right(prefix, text, items_diff, pos_cur)
		elif suffix != self.suffix:
			part = "suffix"

		self.info = f"____ADDITION___[{part}], {info_part}"

		self.update_range()

		new_cur = self.pos_cur + items_diff
		newText = self.get_new_text()

		return newText, new_cur

	def handle_del_part_left(self,prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur):

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

	def handle_del_part_right(self,prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur):

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
			items_diff, info_part = self.handle_del_part_left(prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur)
		elif X != self.X:
			part = "X"
			items_diff, info_part = self.handle_del_part_X(prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur)
		elif mid != self.mid:
			part = "mid"
		elif Y != self.Y:
			part = "Y"
		elif right != self.right:
			part = "right"
			items_diff, info_part = self.handle_del_part_right(prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur)
		elif suffix != self.suffix:
			part = "suffix"

		self.info = f"___FIX_deletion___ --> {part}, {info_part}"

		self.update_range()

		new_cur = self.pos_cur + items_diff
		newText = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix
		return newText, new_cur

	def reset_text(self, text):

		new_cur = 0
		newText = ""

		if len(text) == len(self.prefix) + len(self.X) + len(self.Y) + len(self.suffix) or len(text) == 0:
			newText = ""
			self.maxR = 0
			self.left = ""
			self.right = ""
			self.mid = ""
			self.update_pos_X_Y_num_let(reset=True)
			self.info = f" ____REMOVE____ --> [prefix][number][letter][suffix]"
			self.RenameWidget.LineEditor.AutoComplete_line_edit.setClearButtonEnabled(False)

		else:
			self.maxR   = len(text) + len(self.prefix)
			pos_X       = len(text) + len(self.prefix)
			new_cur     = pos_X
			self.left   = text
			newText     = self.get_new_text()

			# self.update_pos_num_let()

			self.update_pos_X_Y_num_let(items_dift=pos_X, side="X", len_X=0)

			self.info = " ___ADD___ --> [prefix][number][letter][suffix]"
			self.RenameWidget.LineEditor.AutoComplete_line_edit.setClearButtonEnabled(True)

		return newText, new_cur

	def get_new_text(self):
		text = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix
		return text

	def do_text_edited(self, text):

		newText    = ""
		pos_cur    = self.pos_cur
		new_cur     = 0
		items_diff = len(text) - len(self.text)
		prefix, left, X, mid, Y, right, suffix = self.handle_text(text)

		if self.text and len(text) > len(self.prefix)+ len(self.X) + len(self.Y) + len(self.suffix):
			if items_diff > 0:  # Added items

				newText, new_cur = self.handle_addition(prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur)
			elif items_diff < 0:  # Removed items

				newText, new_cur = self.handle_deletion(prefix, left, X, mid, Y, right, suffix, text, items_diff, pos_cur)
		else:
			newText, new_cur = self.reset_text(text)

		self.update_ui_elements(newText, new_cur)

	def update_ui_elements(self, newText, new_cur):
		self.text = newText
		self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(newText)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(new_cur)

		self.NumberWidget.pos_num_slider.setRange(self.minR, self.maxR)
		self.NumberWidget.pos_num_spinbox.setRange(self.minR, self.maxR)
		self.NumberWidget.pos_num_slider.setValue(self.pos_num)
		print("____________________")
		self.NumberWidget.pos_num_spinbox.setValue(self.pos_num)
		print("____________________")
		self.LetterWidget.pos_let_slider.setRange(self.minR, self.maxR)
		self.LetterWidget.pos_let_spinbox.setRange(self.minR, self.maxR)
		self.LetterWidget.pos_let_slider.setValue(self.pos_let)
		self.LetterWidget.pos_let_spinbox.setValue(self.pos_let)

		self.info_attribute()

	def posNumber_cursor(self, oldPos, newPos):
		self.pos_cur = newPos

# TODO перебрать все обновления позиций и заменить на новую фунцию, их две для Х и У подумать, может их объеденить.
# TODO update_pos_X_Y_num_let новая функция.