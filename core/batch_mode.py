import os
from MSL_MayaRename.core.common import log
from MSL_MayaRename.core.resources import Resources
import importlib


root_ = os.path.dirname(__file__)
project_root = os.path.dirname(root_)

class BetchValidator(object):

	def __init__(self):
		self.resource: Resources = Resources.get_instance()
		self.preset_rules = None

	def start(self, preset=None, auto_fix=False):
		self.preset_rules = self.resource.get_preset_rule(preset_name=preset)
		self.run_rules(self.preset_rules, auto_fix)

	def run_rules(self, preset_rules, auto_fix):
		log(message="Run rules.................", category="Start Batch Mode")

		for i in preset_rules:
			log(message="{} run".format(i), category="Rule")
			module_name = "MSL_MayaRename.rules.{}.rule".format(i)

			try:
				rule_module = importlib.import_module(module_name)
				Rule = getattr(rule_module, 'Rule')
				rule = Rule()
				rule_output = rule.check()

			except ModuleNotFoundError as e:
				print(f"Module {module_name} not found: {e}")
			except AttributeError as e:
				print(f"Rule class not found in {module_name}: {e}")

			if rule_output:
				log(message=rule_output, category=i)

				if auto_fix:
					rule.fix()


