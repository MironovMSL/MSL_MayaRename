import maya.cmds as cmds
import maya.mel as mel
from MSL_MayaRename.core.common import log



class Rule(object):
	def __init__(self):
		self.rule_name = "Object History"
		self.rule_description = "All object should not have any history"
		self.output = [] # if output is not empty - the Rule has not been passed

	def check(self):
		self.output = []

		inputStd = ["joint", "tweak", "skinCluster", "mesh", "displayLayer"]
		shapeArray = cmds.ls(type="mesh", dag=1, l=True)

		if shapeArray:
			polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type="transform", f=True)))
			for obj in polyArray:
				tmpListOfinputs = cmds.listHistory(obj, lf=1, il=1) # list object which have inputs
				for i in tmpListOfinputs:
					type = cmds.nodeType(i)
					# if type != "joint" and type != "tweak" and type != "skinCluster" and type != "mesh" and type != "displayLayer"
					if type not in inputStd:
						self.output.append(obj)
						break
			return self.output

	def fix(self):
		if self.output:
			for i in self.output:
				cmds.select(i)
				mel.eval("doBakeNonDefHistory( 1, {\"prePost\"});")
				# deleting polyBlindData node
				tmpListOfinputs = cmds.listHistory(i, lf=1, il=1) # list object which have inputs
				for j in tmpListOfinputs:
					type = cmds.nodeType(j)
					if type == "polyBlindData":
						try:
							cmds.delete(j)
						except:
							pass

		output = self.check()
		return output

