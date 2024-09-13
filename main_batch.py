import maya.standalone
import sys
import os
import maya.cmds as cmds
from argparse import ArgumentParser

FILEPATH = ""


def main():
	# create argument
	# action - means argument comes  without value, we just add it >> hello.py --sui
	parser = ArgumentParser(description="Maya Scene Validator")
	parser.add_argument('-p', '--preset', type=str, required=True, help='Defines with preset you want to use to check maya scenes')
	parser.add_argument('-af', '--auto_fix', type=bool, default=False, help='Should it fix all wrong objects?')
	parser.add_argument('-p', '--path', type=str, required=True, help='Folder path with maya files')
	args = parser.parse_args()

	# ------------------------------------------------
	FILEPATH = args.path
	AUTO_FIX = args.auto_fix
	PRESET = args.preset


	if not os.path.isdir(FILEPATH):
		print("ERROR")
		return

	if not os.listdir(FILEPATH):
		print("ERROR")

	mayaFiles = []

	for i in os.listdir(FILEPATH):
		filename, file_extension = os.path.splitext(i)
		if file_extension == ".mb" or file_extension == ".ma":
			full_path = os.path.join(FILEPATH, i)

			mayaFiles.append(full_path)

	if not mayaFiles:
		print("ERROR")
		return

	maya.standalone.initialize()

	result = {}

	for i in mayaFiles:
		cmds.file(i, open=1)

		import sys
		import importlib

		package_path = 'D:/MironovS/script/GitHub'

		if package_path not in sys.path:
			sys.path.append(package_path)

		packages = ['MSL_MayaRename']

		for i in list(sys.modules.keys()):
			for package in packages:
				if package in i:
					del (sys.modules[i])

		import MSL_MayaRename.main
		from MSL_MayaRename.main import Validator
		MSL_MayaRename.main.main(auto_fix=AUTO_FIX, mode=Validator.BATCH_MODE)

		if AUTO_FIX:
			cmds.file(save=1)

	maya.standalone.uninitialize()


if __name__ == "__main__":
	main()