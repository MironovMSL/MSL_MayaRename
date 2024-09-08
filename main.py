from MSL_MayaRename.core.resources import Resources
import os

root_ = os.path.dirname(__file__)


class Validator(object):
	def __init__(self):
		self.resource = Resources()



def main():
	v = Validator()


if __name__ == '__main__':
	main()
