try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.gui.RenameGUI.FunctionWidget.FunctionWidget import FunctionWidget
from MSL_MayaRename.gui.RenameGUI.RenameWidget.RenameWidget import RenameWidget
from MSL_MayaRename.gui.RenameGUI.RenameWidget.RenameButtonWidget import RenameButtonWidget
from MSL_MayaRename.gui.RenameGUI.NumberWidget.NumberWidget import NumberWidget
from MSL_MayaRename.gui.RenameGUI.LetterWidget.LetterWidget import LetterWidget
from MSL_MayaRename.gui.RenameGUI.SuffixPrefixWidget.SuffixPrefixWidget import SuffixPrefixWidget
from MSL_MayaRename.gui.RenameGUI.LabelWidget.LabelWidget import LabelWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.QuickListButtonNameWidget import QuickListButtonNameWidget
from MSL_MayaRename.gui.RenameGUI.FindReplaceWidget.FindReplaceWidget import FindReplaceWidget

import maya.cmds as cmds
import maya.OpenMaya as om


class RenameGUI(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(RenameGUI, self).__init__(parent)

		# Attribute----------------------
		self.resources   = Resources.get_instance()
		self.QSettings   = QtCore.QSettings(self.resources.config_path, QtCore.QSettings.IniFormat)
		self.FixedHeigt  = 235
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
		self.prefix_num  = None  # prefix of a number
		self.suffix_num  = None  # suffix of a number
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
		self.end_select  = None  # position of a selection name

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
		self.RenameButton        = RenameButtonWidget()
		self.RenameWidget        = RenameWidget()
		self.NumberWidget        = NumberWidget()
		self.LetterWidget        = LetterWidget()
		self.SuffixPrefixWidget  = SuffixPrefixWidget()
		self.QuickListButtonName = QuickListButtonNameWidget()
		self.FindReplaceWidget   = FindReplaceWidget()

	def create_layouts(self):
		# main layout
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)

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
		self.Right_lyout.setAlignment(QtCore.Qt.AlignTop)

		self.main_rename_layout.addLayout(self.left_layout)
		self.main_rename_layout.addLayout(self.Right_lyout)

		# add LabelWidget RenameWidget, NumberWidget, LetterWidget, RenameButton, SuffixPrefixWidget, QuickListButtonNameWidget
		self.main_layout.addWidget(self.FunctionWidget)
		self.main_layout.addWidget(self.LabelWidget)
		self.main_layout.addLayout(self.main_rename_layout)
		self.left_layout.addWidget(self.RenameWidget)
		self.left_layout.addWidget(self.NumberWidget)
		self.left_layout.addWidget(self.LetterWidget)
		self.Right_lyout.addWidget(self.RenameButton)
		self.main_layout.addWidget(self.SuffixPrefixWidget)
		self.main_layout.addWidget(self.QuickListButtonName)
		self.main_layout.addWidget(self.FindReplaceWidget)

		# self.main_layout.addStretch()

	def create_connections(self):
		self.RenameButton.clicked.connect(self.Rename)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.returnPressed.connect(self.Rename)
		self.LabelWidget.number_mode.changeStateNumberMode.connect(self.on_click_number_mode_button)
		self.LabelWidget.number_mode.itPrefixNumber.connect(self.update_prefixNumber)
		self.LabelWidget.number_mode.itSuffixNumber.connect(self.update_suffixNumber)
		self.LabelWidget.number_mode.pop_up_window.letter_mode.itShowLetter.connect(self.on_click_letter_mode)
		self.LabelWidget.button_mode.changeStateButtonMode.connect(self.on_click_button_mode_button)
		self.LabelWidget.find_replace_mode.changeStateFindReplaceMode.connect(self.on_click_find_replace_mode_button)
		self.LetterWidget.itEditLetter.connect(self.update_letter_mode)
		self.LetterWidget.itletPosition.connect(self.move_position_letter)
		self.NumberWidget.new_position_Signal.connect(self.move_position_number)
		self.NumberWidget.new_number_Signal.connect(self.update_number)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.textEdited.connect(self.do_text_edited)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.itDropName.connect(self.drop_text)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.cursorPositionChanged.connect(self.check_position_cursor)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.selectionChanged.connect(self.check_selection_cursor)
		self.RenameWidget.LineEditor.completer.itCompleterName.connect(self.on_complet_name)
		self.RenameWidget.LeftRemoveButton.clicked.connect(self.remove_first_index)
		self.RenameWidget.RightRemoveButton.clicked.connect(self.remove_last_index)
		self.SuffixPrefixWidget.itEditPrefix.connect(self.update_prefix)
		self.SuffixPrefixWidget.itEditSuffix.connect(self.update_suffix)
		self.SuffixPrefixWidget.prefix_Editline.AutoComplete_line_edit.returnPressed.connect(self.add_prefix)
		self.SuffixPrefixWidget.suffix_Editline.AutoComplete_line_edit.returnPressed.connect(self.add_suffix)
		self.SuffixPrefixWidget.prefix_add_btn.clicked.connect(self.add_prefix)
		self.SuffixPrefixWidget.suffix_add_btn.clicked.connect(self.add_suffix)
		self.LabelWidget.label_name.itLabelName.connect(self.get_select_name)
		self.QuickListButtonName.itClickedCache.connect(self.get_select_name)
		self.QuickListButtonName.itClickedName.connect(self.on_click_btn)
		self.QuickListButtonName.itClickedName_alt.connect(self.on_click_btn_alt)
		

	def init_attribute(self):

		# mode----------------------------
		self.mode_button = self.QSettings.value("startup/mode_button", False, bool)  # mode number for button and lineEdits
		self.mode_number = self.QSettings.value("startup/mode_number", False, bool)  # mode number for Numeric
		self.mode_letter = self.QSettings.value("startup/mode_letter", False, bool)
		# number-----------------------------------
		self.prefix_num  = self.resources.config.get_variable("startup", "prefix_number", "", str)
		self.suffix_num  = self.resources.config.get_variable("startup", "suffix_number", "", str)
		self.start_num   = self.QSettings.value("startup/start_number", 1, int)  # start number ~ 1
		self.padding_num = self.QSettings.value("startup/padding_number", 2, int)  # pading number ~ 2 = 00
		self.num         = self.handle_number()  # number start = 1, padding = 2, number = [01]
		self.pos_num     = self.QSettings.value("startup/position_number", 0, int)  # position number [pos:end]
		self.num_cod     = "X"
		# letter----------------------------------
		self.pos_let     = 0  # position letter [pos:end]
		self.let         = self.handel_letter() # letter  ~ [lettter]
		self.let_cod     = "Y"
		# Range and cursor-------------------------------
		self.pos_cur     = 0  # cursor position for comparison
		self.maxR        = 0  # maximum range for position [number] and [letter]
		self.minR        = 0  # minimum range for position [number] and [letter]
		# blocks text------------------------------------
		self.text        = ""  # old text for comperisen [last Text]
		self.prefix, self.suffix  = self.handle_prefix_suffix() # [prefix] [suffix]
		self.left        = ""  # [left]
		self.right       = ""  # [right]
		self.mid         = ""  # [mid]
		# X and Y--------------------------
		self.X           = self.num # [X]
		self.pos_X       = self.pos_num
		self.end_pos_X   = self.pos_X + len(self.X)
		self.Y           = self.let # [Y]
		self.pos_Y       = self.pos_let + len(self.X)
		self.end_pos_Y   = self.pos_Y + len(self.Y)
		# Additional--------------------------
		self.switch_X    = 1
		self.switch_Y    = -1
		self.move        = False
		self.selected    = False
		#------------------------------
		self.info        = "Initialization attribute"

	def info_attribute(self):
		state = False

		if state:
			print("--------------------------------------------")
			print(f"position:{self.num_cod}[{self.pos_num}]-[{self.num}] Number")
			print(f"position:{self.let_cod}[{self.pos_let}]-[{self.let}] Letter")
			print(f"position:X[{self.pos_X}:{self.end_pos_X}]-[{self.X}],")
			print(f"position:Y[{self.pos_Y}:{self.end_pos_Y},{len(self.X)}]-[{self.Y}],")
			print(f"position: [{self.pos_cur}] Cursor")
			print(f"Range: [{self.minR}]:[{self.maxR}]")
			print(f'[{self.prefix}][{self.left}][{self.X}][{self.mid}][{self.Y}][{self.right}][{self.suffix}]: {self.info}')
			print("--------------------------------------------")
	
	def _handle_click_btn(self, name):
		selection = cmds.ls(selection=1, long=1)
		sortName = sorted(selection, key=len, reverse=True)
		
		filtered_list = self.FindReplaceWidget.remove_shapes_from_transforms(sortName)
		
		if filtered_list:
			if name:
				for obj in filtered_list:
					
					path_to_obj, obj_short_name = self.get_short_name(obj)
					
					if obj_short_name[len(obj_short_name) - len(name):] == name:
						continue
					
					new_obj_short_name = obj_short_name + name
					cmds.rename(obj, new_obj_short_name)
				
				self.LabelWidget.update_selection()
			
			else:
				print("The input field is empty. Please enter some text.")
		else:
			print("It is necessary to select an object.")
	
	def _handle_mode_btn_click_btn(self, name):
		name_LE = self.get_text()
		if name_LE:
			if name_LE[len(name_LE) - len(name):] == name:
				return
			new_name_LE = name_LE + name
			self.do_text_edited(new_name_LE)
		else:
			self.do_text_edited(name)
	
	def on_click_btn(self, name):
		name = "_" + name
		if self.mode_button:
			self._handle_mode_btn_click_btn(name)
		else:
			self._handle_click_btn(name)
		
	def on_click_btn_alt(self, name):
		if self.mode_button:
			self._handle_mode_btn_click_btn(name)
		else:
			self._handle_click_btn(name)
	
	def get_short_name(self, object_name):
		path_to_object, separator, object_short_name = object_name.rpartition("|")
		path_to_object += separator
		
		return path_to_object, object_short_name
	
	def Rename(self):
		selection = cmds.ls(selection=True, l=True)
		name_in_LineEdit = self.get_text()
		
		filtered_list = self.FindReplaceWidget.remove_shapes_from_transforms(selection)
		
		if filtered_list:
			if name_in_LineEdit:
				if self.mode_number:
					for start, obj in enumerate(filtered_list, start=self.start_num):
						number = self.handle_number(start)
						
						if self.num_cod == "X":
							name_counting = self.prefix + self.left + number + self.mid + self.Y + self.right + self.suffix
						else:
							name_counting = self.prefix + self.left + self.X + self.mid + number + self.right + self.suffix
						
						path_to_obj, obj_short_name = self.get_short_name(obj)
						obj_rename = cmds.rename(obj, name_counting)
						new_path_to_obj, new_obj_short_name = self.get_short_name(obj_rename)
						new_obj = path_to_obj + new_obj_short_name
						
						filtered_list = self.renameObjectsInHierarchy(filtered_list, obj, new_obj)
	
				else:
					for obj in filtered_list:
						
						path_to_obj, obj_short_name         = self.get_short_name(obj)
						obj_rename = cmds.rename(obj, name_in_LineEdit)
						new_path_to_obj, new_obj_short_name = self.get_short_name(obj_rename)
						new_obj    = path_to_obj + new_obj_short_name
						
						filtered_list = self.renameObjectsInHierarchy(filtered_list, obj, new_obj)
						
				self.LabelWidget.update_selection()
				# -------------Add cashe button-------------
				self.QuickListButtonName.add_cache(name_in_LineEdit)
			
			else:
				print("The input field is empty. Please enter some text.")
		else:
			print("It is necessary to select an object.")
	
	def renameObjectsInHierarchy(self, selection, longName, newlongName):
		"""
		Renames objects in a selection list that match the provided longName,
		updating their hierarchy names with newlongName.
		"""
		
		# Iterate through the selection list and rename matching objects
		for num, obj in enumerate(selection):
			obj_tmp = obj + "|"
			if obj_tmp.startswith(longName + "|"):
				selection[num] = obj.replace(longName, newlongName, 1)
		
		return selection
	
	def remove_first_index(self):
		selection = cmds.ls(selection=1, long=1)
		sortName = sorted(selection, key=len, reverse=True)
		filtered_list = self.FindReplaceWidget.remove_shapes_from_transforms(sortName)
		
		if filtered_list:
			for obj in filtered_list:
				path_to_obj, obj_short_name = self.get_short_name(obj)
				if len(obj_short_name) <= 1:
					om.MGlobal.displayWarning(f"The name cannot be less than one characters: {obj_short_name}")
					continue
	
				try:
					cmds.rename(obj, obj_short_name[1:])
				except:
					om.MGlobal.displayWarning(f"The name cannot be renamed, it has a number next to the letter:  {obj_short_name}")
			
			self.LabelWidget.update_selection()
		
		else:
			print("It is necessary to select an object.")
		
		
	def remove_last_index(self):

		selection = cmds.ls(selection=1, long=1)
		sortName = sorted(selection, key=len, reverse=True)
		filtered_list = self.FindReplaceWidget.remove_shapes_from_transforms(sortName)
		
		if filtered_list:
			for obj in filtered_list:
				path_to_obj, obj_short_name = self.get_short_name(obj)
				if len(obj_short_name) <= 1:
					om.MGlobal.displayWarning(f"The name cannot be less than one characters: {obj_short_name}")
					continue
				
				cmds.rename(obj, obj_short_name[:-1])
			
			self.LabelWidget.update_selection()
			
		else:
			print("It is necessary to select an object.")
			
	def add_prefix(self):
		prefix = self.SuffixPrefixWidget.prefix_Editline.AutoComplete_line_edit.text()
		selection = cmds.ls(selection=1, long=1)
		sortName = sorted(selection, key=len, reverse=True)
		
		filtered_list = self.FindReplaceWidget.remove_shapes_from_transforms(sortName)

		if filtered_list:
			if prefix:
				for obj in filtered_list:
	
					path_to_obj, obj_short_name = self.get_short_name(obj)
	
					if obj_short_name[:len(prefix)] == prefix:
						continue
	
					new_obj_short_name = prefix + obj_short_name
					cmds.rename(obj, new_obj_short_name)
				
				self.LabelWidget.update_selection()
				
			else:
				print("The input field is empty. Please enter some text.")
		else:
			print("It is necessary to select an object.")

	
	def add_suffix(self):
		suffix = self.SuffixPrefixWidget.suffix_Editline.AutoComplete_line_edit.text()
		selection = cmds.ls(selection=1, long=1)
		sortName = sorted(selection, key=len, reverse=True)
		
		filtered_list = self.FindReplaceWidget.remove_shapes_from_transforms(sortName)
		
		if filtered_list:
			if suffix:
				for obj in filtered_list:
					
					path_to_obj, obj_short_name = self.get_short_name(obj)
					
					if obj_short_name[len(obj_short_name) - len(suffix):] == suffix:
						continue
					
					new_obj_short_name = obj_short_name + suffix
					cmds.rename(obj, new_obj_short_name)
				
				self.LabelWidget.update_selection()

			else:
				print("The input field is empty. Please enter some text.")
		else:
			print("It is necessary to select an object.")
	
	def on_complet_name(self, text):
		suffix = text[len(self.text) - len(self.suffix):]
		if suffix == self.suffix and self.suffix:
			self.RenameWidget.LineEditor.completer.popup().hide()
			return

		self.pos_cur = len(text)
		self.do_text_edited(text)

	def get_select_name(self, name):

		text = self.left + self.mid + self.right
		if name and text != name:
			if text:
				button_pressed = QtWidgets.QMessageBox.question(self, "Question", f"Would you like to change the name <span style='color: #669e62; font-size: {12}px;'>{text}</span> to <span style='color: #FF6347; font-size: {12}px;'>{name}</span>?")
				if button_pressed == QtWidgets.QMessageBox.Yes:
					self.do_text_edited("")
					self.do_text_edited(name)
				else:
					print("Cancelled")
			else:
				self.do_text_edited(name)

	def get_text(self):
		return self.RenameWidget.LineEditor.AutoComplete_line_edit.text()

	def check_in_name_suffix(self, text):
		suffix = text[ len(self.text) - len(self.suffix): ]
		print(suffix)
		return

	def get_new_text(self):
		text = self.prefix + self.left + self.X + self.mid + self.Y + self.right + self.suffix
		return text

	def get_end_pos(self, pos, name):
		end_pos = pos + len(name)
		return end_pos

	def update_prefixNumber(self, prefix):
		self.prefix_num = prefix
		self.update_number(self.start_num, self.padding_num)
		
	def update_suffixNumber(self, suffix):
		self.suffix_num = suffix
		self.update_number(self.start_num, self.padding_num)
		
	def handle_number(self, start = None):
		"""Procesing number"""
		start = start if start is not None else self.start_num
		
		if self.mode_number:
			number = self.prefix_num + ("0" * (self.padding_num - len(str(start)))) + str(start) + self.suffix_num
		else:
			number = ""
		return number

	def handle_prefix_suffix(self):
		"""Prefix and Suffix Processing"""
		if self.mode_button:
			prefix = self.SuffixPrefixWidget.prefix_Editline.AutoComplete_line_edit.text()
			suffix = self.SuffixPrefixWidget.suffix_Editline.AutoComplete_line_edit.text()
		else:
			prefix = ""
			suffix = ""

		return prefix, suffix

	def handel_letter(self, letter=None):
		"""Procesing letter"""
		if letter is None:
			letter = self.resources.config.get_variable("startup", "letter", "", str)
			
		if self.mode_letter:
			let = letter
		else:
			let = ""
		return let

	def on_click_letter_mode(self, state):
		self.mode_letter = state
		letter = self.resources.config.get_variable("startup", "letter", "", str)
		self.LetterWidget.set_state_from_letter_mode(state)
		self.update_letter_mode(letter)
		
	def update_letter_mode(self, letter):

		dift             = len(letter)- len(self.let)  # Difference in the length of numerical values
		self.let         = self.handel_letter(letter)
		pos_cur          = self.pos_cur
		text             = self.get_text()
		new_cur          = pos_cur  # Set the initial position of the cursor

		if text:  # If there is text in the field
			if self.let_cod == "X":
				self.X = self.let
				self.update_pos_X_Y_num_let(side="X", len_X=dift)
				new_cur = pos_cur + dift if pos_cur > self.pos_X else new_cur

			elif self.let_cod == "Y":
				self.Y = self.let
				self.update_pos_X_Y_num_let(side="Y")
				new_cur = pos_cur + dift if pos_cur > self.pos_Y else new_cur

			new_text = self.get_new_text()

		else:  # If the field is empty, update only the X or Y values
			if self.let_cod == "X":
				self.X = self.let
				self.update_pos_X_Y_num_let(side="X", len_X=dift)
			elif self.let_cod == "Y":
				self.Y = self.let
				self.update_pos_X_Y_num_let(side="Y")

			new_text = ""

		# Updating text and interface
		self.update_range()
		self.info = f"Letter Mode: {'checked' if self.mode_letter else 'unchecked'}: '{self.let}'"
		self.update_ui_elements(new_text, new_cur)

	def on_click_find_replace_mode_button(self, state):
		self.FindReplaceWidget.show_find_replace(state)
	
	def on_click_number_mode_button(self, state):
		self.NumberWidget.set_state_from_number_mode(state)
		self._state_number(state)

	def on_click_button_mode_button(self, state):
		self.state_prefix_suffix(state)

	def _state_number(self, state):
		dift = len(self.num)  # Difference in the length of numerical values

		self.mode_number = state
		self.num = self.handle_number()

		pos_cur = self.pos_cur
		text = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()
		new_cur = pos_cur  # Set the initial position of the cursor

		if text:  # If there is text in the field
			if self.num_cod == "X":
				self.X = self.num
				self.update_pos_X_Y_num_let(side="Y", len_X=len(self.num) if state else -dift)

				if pos_cur > self.pos_X:
					new_cur = pos_cur + (len(self.X) if state else -dift)

			elif self.num_cod == "Y":
				self.Y = self.num
				self.update_pos_X_Y_num_let(side="Y")
				if pos_cur > self.pos_Y:
					new_cur = pos_cur + (len(self.Y) if state else -dift)

			new_text = self.get_new_text()

		else:  # If the field is empty, update only the X or Y values
			if self.num_cod == "X":
				self.X = self.num
			elif self.num_cod == "Y":
				self.Y = self.num

			new_text = ""

		# Updating text and interface
		self.info = f"Numeric Mode: {'checked' if state else 'unchecked'}: '{self.num}'"
		self.update_ui_elements(new_text, new_cur)

	def state_prefix_suffix(self, state):
		"""Handles a button state change and updates the text and cursor."""
		dift                     = len(self.prefix)
		text                     = self.get_text()
		self.mode_button         = state
		self.prefix, self.suffix = self.handle_prefix_suffix()

		if text:
			new_cur = max(0, self.pos_cur + (len(self.prefix) if state else -dift))
			self.update_pos_X_Y_num_let(side="X", items_dift=(len(self.prefix) if state else -dift))
			new_text = self.get_new_text()
		else:
			new_cur, new_text = 0, ""

		# Updating text and interface
		self.info = f"Button Mode: {'checked' if state else 'unchecked'}: [{self.prefix}]-[{self.suffix}]"
		self.update_range()
		self.update_ui_elements(new_text, new_cur)

	def move_position_letter(self, value):

		value_slider = self.LetterWidget.pos_let_slider.value()
		pos_cur = self.pos_cur
		dift = value - value_slider

		if value_slider == value:
			return

		self.info = (f"Update position letter {value}, {value_slider}!={value}")
		self.move = True
		self.pos_let = value
		if self.pos_num == self.pos_let:
			if dift < 0:
				text = self.prefix + self.left + self.mid + self.right + self.suffix

				self.mid = ""
				self.left = text[len(self.prefix): value]
				self.right =  text[value: len(text) - len(self.suffix)]

				self.pos_Y = value + len(self.X)
				self.update_pos_X_Y_num_let(side="Y")

				self.text = self.get_new_text()

			self.switch_Y = dift
			self.switch_X = -dift

			if dift > 0:
				text = self.prefix + self.left + self.mid + self.right + self.suffix

				self.mid = ""
				self.left = text[len(self.prefix): value]
				self.right = text[value: len(text) - len(self.suffix)]

				self.pos_X = value
				self.update_pos_X_Y_num_let(side="X")

				self.text = self.get_new_text()

			self.switch_Y = dift
			self.switch_X = -dift

		if self.pos_num > self.pos_let:
			text = self.prefix + self.left + self.mid
			self.left = text[len(self.prefix): value]
			self.mid = text[value: self.pos_Y]

			self.pos_X = value

			if self.switch_Y < 0:

				self.X = self.let
				self.Y = self.num
				self.num_cod = "Y"
				self.let_cod = "X"

				self.pos_Y = self.pos_let + len(self.X)

				self.switch_Y = 0
				self.switch_X = 0

			self.update_pos_X_Y_num_let(side="Y")
			self.text = self.get_new_text()

		elif self.pos_num < self.pos_let:
			text = self.prefix + self.left + self.mid + self.right + self.suffix

			self.mid = text[self.pos_X: value]
			self.right = text[value: len(text) - len(self.suffix)]
			self.pos_Y = value + len(self.X)

			if self.switch_Y > 0:

				self.X = self.num
				self.Y = self.let
				self.num_cod = "X"
				self.let_cod = "Y"
				self.switch_Y = 0
				self.switch_X = 0

			self.update_pos_X_Y_num_let(side="Y")
			self.text = self.get_new_text()

		self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(self.text)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(pos_cur)
		self.LetterWidget.pos_let_slider.setValue(value)

		self.move = False
		self.info_attribute()
		self.set_label_rename_color()

	def move_position_number(self, value):

		value_slider         = self.NumberWidget.pos_num_slider.value()
		pos_cur              = self.pos_cur
		dift                 = value - value_slider

		if value_slider == value:
			return

		self.info = (f"Update position number {value}, {value_slider}!={value}")
		self.move = True
		self.pos_num = value

		if self.pos_num == self.pos_let:
			if dift < 0:
				text = self.prefix + self.left + self.mid + self.right + self.suffix

				self.mid = ""
				self.left = text[len(self.prefix): value]
				self.right =  text[value: len(text) - len(self.suffix)]

				self.pos_Y = value + len(self.X)
				self.update_pos_X_Y_num_let(side="Y")

				self.text = self.get_new_text()

			self.switch_X = dift
			self.switch_Y = -dift

			if dift > 0:
				text = self.prefix + self.left + self.mid + self.right + self.suffix

				self.mid = ""
				self.left = text[len(self.prefix): value]
				self.right = text[value: len(text) - len(self.suffix)]

				self.pos_X = value
				self.update_pos_X_Y_num_let(side="X")

				self.text = self.get_new_text()

			self.switch_X = dift
			self.switch_Y = -dift

		elif self.pos_num < self.pos_let:

			text = self.prefix + self.left + self.mid
			self.left = text[len(self.prefix): value]
			self.mid = text[value: self.pos_Y]

			self.pos_X = value

			if self.switch_X < 0:

				self.X = self.num
				self.Y = self.let
				self.num_cod = "X"
				self.let_cod = "Y"

				self.pos_Y = self.pos_let + len(self.X)

				self.switch_X = 0
				self.switch_Y = 0

			self.update_pos_X_Y_num_let(side="Y")
			self.text = self.get_new_text()

		elif self.pos_num > self.pos_let:
			text = self.prefix + self.left + self.mid + self.right + self.suffix

			self.mid = text[self.pos_X: value]
			self.right = text[value: len(text) - len(self.suffix)]
			self.pos_Y = value + len(self.X)

			if self.switch_X > 0:

				self.X = self.let
				self.Y = self.num
				self.num_cod = "Y"
				self.let_cod = "X"

				self.switch_X = 0
				self.switch_Y = 0

			self.update_pos_X_Y_num_let(side="Y")
			self.text = self.get_new_text()

		self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(self.text)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(pos_cur)
		self.NumberWidget.pos_num_slider.setValue(value)


		self.move = False
		self.set_label_rename_color()
		self.info_attribute()

	def update_number(self, start_number, padding_number):
		
		old_num           = self.num
		self.start_num    = start_number
		self.padding_num  = padding_number
		self.num          = self.handle_number()

		text              = self.RenameWidget.LineEditor.AutoComplete_line_edit.text()
		pos_cur           = self.pos_cur
		new_cur           = pos_cur  # Set the initial position of the cursor
		dift              = len(self.num) - len(old_num)

		if text: # If there is text in the field
			if self.num_cod == "X":
				self.X = self.num
				self.update_pos_X_Y_num_let(side="X", len_X=dift)
				if pos_cur > self.pos_X:
					new_cur = pos_cur + dift

			elif self.num_cod == "Y":
				self.Y = self.num
				self.update_pos_X_Y_num_let(side="Y")

				if pos_cur > self.pos_Y:
					new_cur = pos_cur + dift

			newText = self.get_new_text()

		else:  # If the field is empty, update only the X or Y values
			if self.num_cod == "X":
				self.X = self.num
			elif self.num_cod == "Y":
				self.Y = self.num
			newText = ""

		self.info = (f'New number: {self.num}, start: {self.start_num}, padding: {self.padding_num}')
		self.update_ui_elements(newText, new_cur)

	def update_prefix(self, prefix):
		dift = len(prefix) - len(self.prefix)
		text = self.get_text()
		self.prefix, self.suffix = self.handle_prefix_suffix()

		if self.mode_button:
			self.info = (f'New prefix: [{self.prefix}]')
			if text:
				new_text = self.get_new_text()
				new_cur = self.pos_cur + dift
				self.update_pos_X_Y_num_let(side="X", items_dift=dift)
				self.update_range()
				self.update_ui_elements(new_text, new_cur)
		else:
			self.info = (f'Button mode "{self.mode_button}", Initialization prefix: [{prefix}]')
			self.info_attribute()

		self.set_label_rename_color()

	def update_suffix(self, suffix):
		text                     = self.get_text()
		self.prefix, self.suffix = self.handle_prefix_suffix()

		if self.mode_button:
			if text:
				self.text = self.get_new_text()
				new_cur = self.pos_cur
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(self.text)
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(new_cur)


			self.info = (f'New suffix: [{self.suffix}]')
		else:
			self.info = (f'Button mode {self.mode_button}, Initialization suffix: [{suffix}]')


		self.info_attribute()
		self.set_label_rename_color()

	def update_range(self):
		self.maxR = len(self.prefix) + len(self.left) + len(self.mid) + len(self.right)
		self.minR = len(self.prefix)

	def update_pos_X_Y_num_let(self, items_dift = 0, side="X", len_X = 0, reset = False):

		if reset:
			self.pos_X      = 0
			self.end_pos_X  = self.get_end_pos(self.pos_X, self.X)
			self.pos_Y      = self.end_pos_X
			self.end_pos_Y  = self.get_end_pos(self.pos_Y, self.Y)

			self.pos_num    = 0
			self.pos_let    = 0

		else:
			if side == "X":
				self.pos_X     = self.pos_X + items_dift
				self.end_pos_X = self.get_end_pos(self.pos_X, self.X)
				self.pos_Y     = self.pos_Y + items_dift + len_X
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

	def do_text_edited(self, text):
		items_dift = len(text) - len(self.text)
		pos_cur    = self.pos_cur

		if self.text and len(text) > len(self.prefix)+ len(self.X) + len(self.Y) + len(self.suffix):
			if items_dift >= 0:  # Added items
				newText, new_cur = self._handle_addition(text, items_dift, pos_cur)
			elif items_dift < 0:  # Removed items
				newText, new_cur = self._handle_deletion(text, items_dift, pos_cur)
		else:
			newText, new_cur = self._reset_text(text, items_dift)

		self.update_ui_elements(newText, new_cur)

	def _handle_addition(self, text, items_dift, pos_cur):

		prefix_end = len(self.prefix)
		left_end   = prefix_end + len(self.left)
		x_end      = left_end + len(self.X)
		mid_end    = x_end + len(self.mid)
		y_end      = mid_end + len(self.Y)
		right_end  = y_end + len(self.right)
		suffix_end = right_end + len(self.suffix)

		if pos_cur > len(self.text):
			pos_cur = len(self.text)

		if 0 <= pos_cur < prefix_end:
			info_part  = (f"[PREFIX] --> NO Change [{self.prefix}]: {list(range(0, prefix_end))}")
			items_dift = 0

		elif prefix_end <= pos_cur <= left_end:
			self.update_pos_X_Y_num_let(items_dift=items_dift, side="X")
			self.left = text[len(self.prefix): left_end + items_dift]
			info_part = (f"[LEFT] Change [{self.left}]: {list(range(prefix_end, left_end + items_dift))}")

		elif left_end < pos_cur < x_end:
			info_part  = (f"[X] --> NO Change [{self.X}]: {list(range(left_end, x_end))}")
			items_dift = 0

		elif x_end <= pos_cur <= mid_end:
			self.update_pos_X_Y_num_let(items_dift=items_dift, side="Y")
			self.mid = text[ x_end : mid_end + items_dift ]
			info_part = (f"[MID] Change [{self.mid}]: {list(range(x_end, mid_end + items_dift))}")

		elif mid_end < pos_cur < y_end:
			info_part = (f"[Y] --> NO Change [{self.Y}]: {list(range(mid_end, y_end))}")
			items_dift = 0

		elif y_end <= pos_cur <= right_end:
			self.right = text[y_end: right_end + items_dift]
			info_part = (f"[RIGHT] Change [{self.right}]: {list(range(y_end, right_end + items_dift))}")

		elif right_end < pos_cur <= suffix_end:
			info_part = (f"[SUFFIX] --> NO Change [{self.suffix}]: {list(range(right_end, suffix_end))}")
			items_dift = 0

		new_cur   = self.pos_cur + items_dift
		newText   = self.get_new_text()
		self.info = f"__ADD__{info_part}"

		self.update_range()

		return newText, new_cur

	def _handle_deletion(self, text, items_dift, pos_cur):
		temp_cur   = self.RenameWidget.LineEditor.AutoComplete_line_edit.cursorPosition()
		prefix_end = len(self.prefix)
		left_end   = prefix_end + len(self.left)
		x_end      = left_end + len(self.X)
		mid_end    = x_end + len(self.mid)
		y_end      = mid_end + len(self.Y)
		right_end  = y_end + len(self.right)
		suffix_end = right_end + len(self.suffix)
		
		info_part  = ""
		
		if self.selected:
			pos_cur = self.end_select
		
		if temp_cur != pos_cur:

			if 0 < pos_cur <= prefix_end: # [prefix]
				info_part = (f"[PREFIX] --> NO Change [{self.prefix}]: {list(range(0, prefix_end))}")
				items_dift = 0

			elif prefix_end < pos_cur <= left_end: #[left]
				self.update_pos_X_Y_num_let(items_dift=items_dift, side="X")
				self.left = text[len(self.prefix): left_end + items_dift]
				info_part = (f"[LEFT] Change [{self.left}]: {list(range(prefix_end, left_end + items_dift))}")

			elif left_end < pos_cur <= x_end: # [X]
				if self.left:
					self.update_pos_X_Y_num_let(items_dift=items_dift, side="X")
					self.left = text[len(self.prefix): left_end + items_dift]
					info_part = (f"[X] --> NO Change [{self.X}]: {list(range(left_end, x_end))}, left = True [{self.left}]")

				else:
					info_part = (f"[X] --> NO Change [{self.X}]: {list(range(left_end, x_end))}, left = False [{self.left}]")
					items_dift = 0

			elif x_end < pos_cur <= mid_end: # [mid]
				self.update_pos_X_Y_num_let(items_dift=items_dift, side="Y")
				self.mid = text[x_end: mid_end + items_dift]
				info_part = (f"[MID] Change [{self.mid}]: {list(range(x_end, mid_end + items_dift))}")

			elif mid_end < pos_cur <= y_end: # [Y]

				if self.mid:
					self.update_pos_X_Y_num_let(items_dift=items_dift, side="Y")
					self.mid = text[x_end: mid_end + items_dift]
					info_part = (f"[Y] --> NO Change [{self.Y}]: {list(range(mid_end, y_end))}, mid = True [{self.mid}]")

				elif self.left:
					self.update_pos_X_Y_num_let(items_dift=items_dift, side="X")
					self.left = text[len(self.prefix): left_end + items_dift]
					info_part = (f"[Y] --> NO Change [{self.Y}]: {list(range(mid_end, y_end))}, mid = False [{self.mid}], left = True [{self.left}]")

				else:
					info_part = (f"[Y] --> NO Change [{self.Y}]: {list(range(mid_end, y_end))}, mid = False [{self.mid}], left = False [{self.left}]")
					items_dift = 0

			elif y_end < pos_cur <= right_end: # [right]
				self.right = text[y_end: right_end + items_dift]
				info_part = (f"[RIGHT] Change [{self.right}]: {list(range(y_end, right_end + items_dift))}")

			elif right_end < pos_cur <= suffix_end:
				info_part = (f"[SUFFIX] --> NO Change [{self.suffix}]: {list(range(right_end, suffix_end))}")
				items_dift = 0

		else:

			if 0 <= pos_cur < prefix_end: # [prefix]
				info_part = (f"[PREFIX] --> NO Change [{self.prefix}]: {list(range(0, prefix_end))}")

			elif prefix_end <= pos_cur < left_end: # [left]
				self.update_pos_X_Y_num_let(items_dift=items_dift, side="X")
				self.left = text[len(self.prefix): left_end + items_dift]
				info_part = (f"[LEFT] Change [{self.left}]: {list(range(prefix_end, left_end + items_dift))}")

			elif left_end <= pos_cur < x_end: # [X]
				if self.mid:
					self.update_pos_X_Y_num_let(items_dift=items_dift, side="Y")
					self.mid   = text[x_end: mid_end + items_dift]
					info_part  = (f"[X] --> NO Change [{self.X}]: {list(range(left_end, x_end))}, mid = True [{self.mid}]")

				elif self.right:
					self.right = text[y_end: right_end + items_dift]
					info_part = (f"[X] --> NO Change [{self.X}]: {list(range(left_end, x_end))}, mid = False [{self.mid}], right = True [{self.right}]")

				else:  # left side >|[X]
					info_part = (f"[X] --> NO Change [{self.X}]: {list(range(left_end, x_end))}, mid = False [{self.mid}], right = False [{self.right}]")

			elif x_end <= pos_cur < mid_end: # [mid]
				self.update_pos_X_Y_num_let(items_dift=items_dift, side="Y")
				self.mid = text[x_end: mid_end + items_dift]
				info_part = (f"[MID] Change [{self.mid}]: {list(range(x_end, mid_end + items_dift))}")

			elif mid_end <= pos_cur < y_end: # [Y]
				info_part = (f"[Y] --> NO Change [{self.Y}]: {list(range(mid_end, y_end))}")

				if self.right:
					self.right = text[y_end: right_end + items_dift]
					info_part = (f"[Y] --> NO Change [{self.Y}]: {list(range(mid_end, y_end))}, right = True [{self.right}]")

				else:  # left side >|[X]
					info_part = (f"[Y] --> NO Change [{self.Y}]: {list(range(mid_end, y_end))}, right = False [{self.right}]")

			elif y_end <= pos_cur < right_end:  # [right]
				self.right = text[y_end: right_end + items_dift]
				info_part = (f"[RIGHT] Change [{self.right}]: {list(range(y_end, right_end + items_dift))}")

			elif right_end <= pos_cur < suffix_end:
				info_part = (f"[SUFFIX] --> NO Change [{self.suffix}]: {list(range(right_end, suffix_end))}")

			items_dift = 0

		new_cur   = pos_cur + items_dift
		newText   = self.get_new_text()
		self.info = f"__DEL__{info_part}"

		self.update_range()

		return newText, new_cur

	def _reset_text(self, text, items_dift):
		if items_dift > 0:
			self.left   = text
			self.minR   = len(self.prefix)
			self.maxR   = len(text) + len(self.prefix)
			pos_X       = len(text) + len(self.prefix)
			new_cur     = len(text) + len(self.prefix)
			newText     = self.get_new_text()

			self.update_pos_X_Y_num_let(items_dift=pos_X, side="X", len_X=0)
			self.RenameWidget.LineEditor.AutoComplete_line_edit.setClearButtonEnabled(True)
			self.info = " ___ADD___ --> [prefix][number][letter][suffix]"

		else:
			new_cur    = 0
			newText    = ""
			self.left  = ""
			self.right = ""
			self.mid   = ""
			self.minR  = 0
			self.maxR  = 0

			self.update_pos_X_Y_num_let(reset=True)
			self.RenameWidget.LineEditor.AutoComplete_line_edit.setClearButtonEnabled(False)
			self.info = f" ____REMOVE____ --> [prefix][number][letter][suffix]"

		return newText, new_cur

	def update_ui_elements(self, newText, new_cur):

		self.text = newText
		self.RenameWidget.LineEditor.AutoComplete_line_edit.setText(newText)
		self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(new_cur)

		self.NumberWidget.pos_num_slider.setRange(self.minR, self.maxR)
		self.NumberWidget.pos_num_spinbox.setRange(self.minR, self.maxR)
		self.LetterWidget.pos_let_slider.setRange(self.minR, self.maxR)
		self.LetterWidget.pos_let_spinbox.setRange(self.minR, self.maxR)

		self.NumberWidget.pos_num_slider.setValue(self.pos_num)
		self.NumberWidget.pos_num_spinbox.setValue(self.pos_num)
		self.LetterWidget.pos_let_slider.setValue(self.pos_let)
		self.LetterWidget.pos_let_spinbox.setValue(self.pos_let)

		self.info_attribute()
		self.set_label_rename_color()

	def drop_text(self, text, pos_cur):
		suffix = text[len(self.text) - len(self.suffix):]

		if suffix == self.suffix and self.suffix:
			self.RenameWidget.LineEditor.completer.popup().hide()
			return

		self.pos_cur = pos_cur
		self.do_text_edited(text)

	def check_position_cursor(self, oldPos, newPos):
		self.pos_cur = newPos

		if  self.move:
			return

		if self.selected:
			self.selected = False
			return

		pos_cur      = self.pos_cur
		dift         = newPos - oldPos
		prefix_end   = len(self.prefix)
		left_end     = prefix_end + len(self.left)
		x_end        = left_end + len(self.X)
		mid_end      = x_end + len(self.mid)
		y_end        = mid_end + len(self.Y)
		right_end    = y_end + len(self.right)
		suffix_end   = right_end + len(self.suffix)

		if 0 <= pos_cur < prefix_end:
			self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(prefix_end)
		elif left_end < pos_cur < x_end:
			if dift < 0:
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(left_end)
			if dift > 0:
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(x_end)
		elif mid_end < pos_cur < y_end:
			if dift < 0:
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(mid_end)
			if dift > 0:
				self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(y_end)
		elif right_end < pos_cur <= suffix_end:
			self.RenameWidget.LineEditor.AutoComplete_line_edit.setCursorPosition(right_end)

	def check_selection_cursor(self):
		start = self.RenameWidget.LineEditor.AutoComplete_line_edit.selectionStart()
		selected_text  = self.RenameWidget.LineEditor.AutoComplete_line_edit.selectedText()
		
		if selected_text:
			self.selected = True
			self.end_select = start + len(selected_text)
		
	def set_label_rename_color(self):
		self.LabelWidget.label_name.set_rename_color(self.text, self.prefix, self.left, self.X, self.mid, self.Y, self.right, self.suffix)