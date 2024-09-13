
from MSL_MayaRename.gui.main_gui import ValidatorGui, creat_gui
from MSL_MayaRename.core.batch_mode import BetchValidator
import os


root_ = os.path.dirname(__file__)


class Validator(object):

	GUI_Mode = 0
	BATCH_MODE = 1

	def __init__(self, mode, preset, auto_fix=False):


		if mode == Validator.GUI_Mode:
			creat_gui()
		elif mode == Validator.BATCH_MODE:
			batch = BetchValidator()
			batch.start(preset=preset, auto_fix=False)


def main(preset="modeling", auto_fix=False, mode=Validator.GUI_Mode):
	v = Validator(mode=mode, preset=preset,auto_fix=auto_fix)

# if __name__ == '__main__':
# 	# main()
