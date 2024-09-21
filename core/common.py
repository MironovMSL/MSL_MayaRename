import json
import os


root_ = os.path.dirname(__file__) # ...\MSL_MayaRename\core
new_root = os.path.abspath(os.path.join(root_, '..')) # ...\MSL_MayaRename


def read_json(path=None):
	assert path is not None, "path is None"
	with open(path, 'r') as json_file:
		json_data = json.load(json_file)
	return json_data

def all_list_itemJSON():

	word_list = []
	Data_Json =read_json(os.path.join(new_root,"gui", "resources", "listButtonsName.json"))

	for key, value in Data_Json.items():
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

