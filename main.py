from MSL_MayaRename.core.config import Configurator
import os

root_ = os.path.dirname(__file__)


class Validator(object):
	def __init__(self):
		self.config = Configurator(config_path=os.path.join(root_, "config.ini"))


def main():
	Validator()


if __name__ == '__main__':
	main()
