import json

def log(message="", category=""):
	"""
	Prints some useful information
	:param message: the message
	:param category: where this message  comes from
	:return: None
	"""

	print ("[VALIDATOR {0}] {1}".format(category, message))


def read_json(path=None):
	assert path is not None, "path is None"
	with open(path, 'r') as json_file:
		json_data = json.load(json_file)
	return json_data