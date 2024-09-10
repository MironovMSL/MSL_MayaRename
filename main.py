
from MSL_MayaRename.gui.main_gui import ValidatorGui, creat_gui
import os


root_ = os.path.dirname(__file__)


class Validator(object):

	GUI_Mode = 0
	BATCH_MODE = 1

	def __init__(self, mode):


		if mode == Validator.GUI_Mode:
			creat_gui()
		elif mode == Validator.BATCH_MODE:
			pass


def main():
	v = Validator(mode=Validator.GUI_Mode)

# if __name__ == '__main__':
# 	# main()
