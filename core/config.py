from configparser import ConfigParser
import os

root_ = os.path.dirname(__file__)


class Configurator(object):
	"""
	Class work with config.ini
	"""

	def __init__(self, config_path):
		self.config_path = config_path
		self.config = ConfigParser()
		self.config.read(self.config_path)

	def set_variable(self, section=None, var_name=None, value=None):

		assert var_name is not None, "var_name is None"
		assert value is not None, "value is None"
		assert section is not None, "section is None"

		if section:
			if not self.config.has_section(section):
				self.config.add_section(section)
			self.config.set(section, var_name, value)
		else:
			self.config.set("custom", var_name, value)

		self.write_config()

	def get_variable(self, section=None, var_name=None):
		assert var_name is not None, "var_name is None"
		assert section is not None, "section is None"

		return self.config.get(section, var_name)

	def get_current_preset(self):
		return self.config.get("startup", "current_preset")

	def get_current_preset_path(self):
		return self.config.get("startup", "current_preset_path")

	def set_current_preset(self, preset=None):
		assert preset is not None, "preset is None"
		self.config.set("startup", "current_preset", preset)
		self.write_config()

	def set_current_preset_path(self, preset_path=None):
		assert preset_path is not None, "preset is None"
		self.config.set("startup", "current_preset_path", preset_path)
		self.write_config()

	def init_config(self):
		if not self.config:
			return

		# create section "startup"
		if not self.config.has_section("startup"):
			self.config.add_section("startup")

		# create current preset
		try:
			current_preset = self.get_current_preset()
		except:
			self.config.set("startup", "current_preset", "test")

		# create current presetPath
		try:
			current_preset = self.get_current_preset_path()
		except:
			self.config.set("startup", "current_preset_path", os.path.join(root_, "presets", "test.json"))

		self.write_config()

	def write_config(self):
		with open(self.config_path, 'w') as config_file:
			self.config.write(config_file)
