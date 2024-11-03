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
		self.all_item_json = [] # list all name from JSON
		self.config: Configurator = None

		self.get_config()
		self.get_info()
		self.get_all_itemJSON()


	def get_config(self):
		"""
		Creates configurator class instance
		:return: None
		"""
		self.config = Configurator(config_path=self.config_path)
		self.config.init_config()
		self.config.get_info_all_keys()

	def get_all_itemJSON(self):

		self.all_item_json = []
		data_json = self.read_json(os.path.join(self.listButtonsName_json_path))

		for key, value in data_json.items():
			if isinstance(value, list):  # Check if a value is a list
				for item in value:
					if item not in self.all_item_json:
						self.all_item_json.append(item)
			elif isinstance(value, dict):  # If the nested elements are dictionaries, we also iterate over them
				for sub_key, sub_value in value.items():
					if isinstance(sub_value, list):
						for item in sub_value:
							if item not in self.all_item_json:
								self.all_item_json.append(item)
		return self.all_item_json

	def read_json(self, path=None):
		assert path is not None, "path is None"

		file = QtCore.QFile(path)
		if not file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			raise Exception(f"Failed to open file: {path}")

		json_data = file.readAll()
		file.close()

		json_doc = QtCore.QJsonDocument.fromJson(json_data)
		if json_doc.isNull():
			raise ValueError("Invalid JSON format")

		return json_doc.toVariant()

	def get_itemJSON_from_key(self, dictionary_name):
		"""
		 Retrieves a list of words from a JSON file by the specified key.
	    """
		word_list = []
		data_json = self.read_json(os.path.join(root_, "resources", "listButtonsName.json"))

		if dictionary_name in data_json:  # Check if the given dictionary exists in JSON
			word_list = data_json[dictionary_name]

		return word_list

	def get_icon_from_resources(self, name=""):
		"""
		Retrieves an icon from the resources directory by the specified name.
		"""
		icon = QtGui.QIcon(os.path.join(root_, "resources", "icon", name))
		return icon

	def get_info(self):

		log(message=f"config path = {self.config_path}", category="config.ini")
		log(message=f"icon path = {self.icon_path}", category="icon")
		log(message=f"listButtonsName path = {self.listButtonsName_json_path}", category="listButtonsName.json")



