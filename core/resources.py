from MSL_MayaRename.core.config import Configurator
from MSL_MayaRename.core.common import *
import os

root_ = os.path.dirname(__file__)
project_root_ = os.path.dirname(root_) # .../MSL_MayaRename


class Resources(object):
	__instance__ = None

	@staticmethod
	def get_instance():
		if not Resources.__instance__:
			Resources()
		return Resources.__instance__

	def __init__(self):
		if Resources.__instance__ is None:
			Resources.__instance__ = self
		else:
			raise Exception("Error Singleton")

		self.config_path = os.path.join(project_root_, "config.ini")  # config.ini path
		self.icon_path = os.path.join(root_, "resources", "icon")  # icon path
		self.listButtonsName_json_path = os.path.join(root_, "resources", "listButtonsName.json")  # listButtonsName.json path
		self.config: Configurator = None

		self.get_config()
		self.get_info()

	def get_config(self):
		"""
		Creates configurator class instance
		:return: None
		"""
		self.config = Configurator(config_path=self.config_path)
		self.config.init_config()
		self.config.get_info_all_keys()


	def save_current_preset(self, preset=None):
		assert preset is not None, "preset is None"
		self.config.set_current_preset(preset=preset)

		for preset_path in self.preset_paths:
			if preset + ".json" in preset_path:
				self.config.set_current_preset_path(preset_path=preset_path)
				break

	def get_info(self):

		log(message=f"config path = {self.config_path}", category="config.ini")
		log(message=f"icon path = {self.icon_path}", category="icon")
		log(message=f"listButtonsName path = {self.listButtonsName_json_path}", category="listButtonsName.json")



