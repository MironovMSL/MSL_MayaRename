try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

import json
import os


root_ = os.path.dirname(__file__) # ...\MSL_MayaRename\core
new_root = os.path.abspath(os.path.join(root_, '..')) # ...\MSL_MayaRename

def log(message="", category=""):
	"""
	Prints some useful information
	:param message: the message
	:param category: where this message  comes from
	:return: None
	"""

	print ("[MSL: {0}] {1}".format(category, message))


def read_json(path=None):
	assert path is not None, "path is None"
	with open(path, 'r') as json_file:
		json_data = json.load(json_file)
	return json_data

def all_list_itemJSON():

	word_list = []
	data_json = read_json(os.path.join(root_, "resources", "listButtonsName.json"))

	for key, value in data_json.items():
		if isinstance(value, list): # Check if a value is a list
			for item in value:
				if item not in word_list:
					word_list.append(item)
		elif isinstance(value, dict): # If the nested elements are dictionaries, we also iterate over them
			for sub_key, sub_value in value.items():
				if isinstance(sub_value, list):
					for item in sub_value:
						if item not in word_list:
							word_list.append(item)
	return word_list

def get_list_itemJSON(dictionary_name):
	word_list = []
	data_json = read_json(os.path.join(root_, "resources", "listButtonsName.json"))

	if dictionary_name in data_json: # Check if the given dictionary exists in JSON
		word_list = data_json[dictionary_name]

	return word_list

def get_icon_from_resources(name=""):
	icon = QtGui.QIcon(os.path.join(root_, "resources", "icon", name))
	return icon
