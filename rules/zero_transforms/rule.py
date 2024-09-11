import maya.cmds as cmds
import maya.mel as mel
from MSL_MayaRename.core.common import log


class Rule(object):
	def __init__(self):

		self.rule_name = "Object Transform"
		self.rule_description = "All objects should have all transform zeroed out"

		self.output = []# # if output is not empty - the Rule has not been passed

	def check(self):

		self.output = []

		# get all transform in our scene
		allTransform = cmds.ls(type="transform", l=1)
		cameras = cmds.ls(type="camera", l=1)
		camerasTransform = cmds.listRelatives(cameras, p=1, f=1)

		for i in allTransform:
			if i in camerasTransform:
				continue

			t = cmds.xform(i, q=1, t=1, a=1)
			r = cmds.xform(i, q=1, ro=1, a=1)
			s = cmds.xform(i, q=1, s=1, r=1)

			if t != [0.0, 0.0, 0.0] or r !=[0.0, 0.0, 0.0] or s != [1, 1, 1]:
					self.output.append(i)

		return self.output

	def fix(self):
		if self.output:

			for i in self.output:
				cmds.xform(i, t=[0, 0, 0])
				cmds.xform(i, ro=[0, 0, 0])
				cmds.xform(i, s=[1, 1, 1])

		output = self.check()
		return output
