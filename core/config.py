try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore
from MSL_MayaRename.core.common import *
import os

class Configurator(object):
	"""
	Class work with config.ini
	"""
	def __init__(self, config_path):

		self.config_path = config_path
		self.config = QtCore.QSettings(self.config_path, QtCore.QSettings.IniFormat)

	def set_variable(self, section=None, var_name=None, value=None):
		"""
		Set a variable in the config file.
		:param section: Group or section in the config (used as a group in QSettings)
		:param var_name: Name of the variable
		:param value: Value to set for the variable
		"""
		assert var_name is not None, "var_name is None"
		assert value is not None, "value is None"
		assert section is not None, "section is None"

		self.config.beginGroup(section)
		self.config.setValue(var_name, value)
		self.config.endGroup()

	def get_variable(self, section=None, var_name=None, default_value=None, type=None):
		"""
		Get a variable from the config file.
		:param section: Group or section in the config (used as a group in QSettings)
		:param var_name: Name of the variable
		:param default_value: Default value if the variable does not exist
		:return: The value of the variable or default_value
		"""
		assert var_name is not None, "var_name is None"
		assert section is not None, "section is None"
		assert type is not None, "type is None"

		self.config.beginGroup(section)
		value = self.config.value(var_name, default_value, type)
		self.config.endGroup()
		return value

	def init_config(self):
		"""
		Initialize default configuration if it does not exist.
		"""
		# Initialize the "All" group and set default values
		if not self.config.contains("startup/name_tool"):

			self.config.beginGroup("startup") # startup group
			
			self.config.setValue("name_tool", "MSL Rename")
			self.config.setValue("window_geometry", "")
			self.config.setValue("name", "test")
			self.config.setValue("mode_number", False)
			self.config.setValue("mode_button", False)
			self.config.setValue("mode_letter", False)
			self.config.setValue("mode_find_replace", False)
			self.config.setValue("start_number", 1)
			self.config.setValue("padding_number", 2)
			self.config.setValue("position_number", 0)
			self.config.setValue("number", "01")
			self.config.setValue("letter", "")
			self.config.setValue("prefix", "")
			self.config.setValue("suffix", "")
			self.config.setValue("prefix_number", "")
			self.config.setValue("suffix_number", "")

			self.config.endGroup()  # End the group

			self.config.beginGroup("selected_objects") # selected_objects group

			self.config.setValue("selected_mode", False)

			self.config.endGroup() # End the group

			self.config.beginGroup("library")  # library group

			self.config.setValue("library_mode", False)
			self.config.setValue("category_mode", False)
			self.config.setValue("sub_category_mode", False)
			self.config.setValue("current_category", "Postfixes")
			self.config.setValue("show_cache", False)

			self.config.endGroup()  # End the group

	def get_info_all_keys(self):
			# print config.ini
			keys = self.config.allKeys()

			for key in keys:
				value = self.config.value(key)
				parts = key.split('/')

				log(message=f"[{parts[0]}] {parts[1]} = {value}", category="config.ini")

