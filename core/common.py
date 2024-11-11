try:
	from PySide2 import QtWidgets, QtGui, QtCore
except:
	from PySide6 import QtWidgets, QtGui, QtCore

import json
import os
import random

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

# def read_json(path=None):
# 	assert path is not None, "path is None"
# 	with open(path, 'r') as json_file:
# 		json_data = json.load(json_file)
# 	return json_data

def get_icon_from_resources(name=""):
	icon = QtGui.QIcon(os.path.join(root_, "resources", "icon", name))
	return icon

def read_json(path=None):
	assert path is not None, "path is None"

	file = QtCore.QFile(path)
	if not file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
		raise Exception(f"Failed to open file: {path}")

	json_data = file.readAll()
	file.close()

	json_doc = QtCore.QJsonDocument.fromJson(json_data)
	if json_doc.isNull():
		raise ValueError("Invalid JSON format")

	return json_doc.toVariant()  # Converts JSON to Python dictionary format

def get_list_itemJSON(dictionary_name):
	word_list = []
	data_json = read_json(os.path.join(root_, "resources", "listButtonsName.json"))

	if dictionary_name in data_json: # Check if the given dictionary exists in JSON
		word_list = data_json[dictionary_name]

	return word_list
	
def generate_random_color(self):
	# Генерируем случайные значения для R, G, B
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	
	# Формируем строку цвета в формате hex (#RRGGBB)
	color = f"#{r:02x}{g:02x}{b:02x}"
	return color