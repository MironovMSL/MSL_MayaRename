import maya.standalone
import sys
import os
import maya.cmds as cmds
from argparse import ArgumentParser

FILEPATH = ""


def main():
	# create argument
	# action - means argument comes  without value, we just add it >> hello.py --sui
	parser = ArgumentParser(description="This script freezes _cn_ curves")
	parser.add_argument('-p', '--path', type=str, required=True, help='Defind a path where all Maya files have to be fixed')
	parser.add_argument('-nt', '--nodeType', type=str, default='nurbsCurve', help='Type of node to be freezed')
	args = parser.parse_args()


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

		listofCurve = cmds.ls(type="nurbsCurve", l=1)
		listofCurveTransforms = cmds.listRelatives(listofCurve, p=1, f=1) #[]

		fileShortName = i.split('\\')[-1]
		result[fileShortName] = []

		for j in listofCurveTransforms:
			if '_cn_' in j:
				cmds.makeIdentity(j, t=1, s=1, r=1)
				result[fileShortName].append(j)

		cmds.file(save=1)

	maya.standalone.uninitialize()

	for key, value in result.item():
		print("\n" + key)
		if isinstance(value, list):
			if value:
				for i in value:
					print("\t" + i)
			else:
				print ("\t" + "No curve found")

if __name__ == "__main__":
	main()