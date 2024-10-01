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
	Data_Json = read_json(os.path.join(new_root,"gui", "resources", "listButtonsName.json"))

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

def get_list_itemJSON(dictionary_name=str):
	word_list = []
	data_json = read_json(os.path.join(new_root, "gui", "resources", "listButtonsName.json"))

	if dictionary_name in data_json: # Check if the given dictionary exists in JSON
		target_dict = data_json[dictionary_name]

		if isinstance(target_dict, dict):
			for key, value in target_dict.items():

				if isinstance(value, list): # If value is a list
					for item in value:
						if item not in word_list:
							word_list.append(item)
				elif isinstance(value, dict): # If value is a dictionary
					for sub_key, sub_value in value.items():
						if isinstance(sub_value, list):
							for item in sub_value:
								if item not in word_list:
									word_list.append(item)
				elif isinstance(value, (str, int, float)): # If value is a single element
					if value not in word_list:
						word_list.append(value)

		elif isinstance(target_dict, list): # If the value by key is a list
			for item in target_dict:
				if item not in word_list:
					word_list.append(item)

		elif isinstance(target_dict, (str, int, float)): # If the value by key is a single element (string, number, etc.)
			if target_dict not in word_list:
				word_list.append(target_dict)

	return word_list

