from abc import ABC, abstractmethod


'''
Abstract command class.
'''
class AbstractCommand(ABC):

	'''
	Command constructor.

	Each command will take a specific set of options that will be used to execute the command.
	'''
	@abstractmethod
	def __init__(self, options):
		pass


	'''
	Execute the command.

	Execute the command on the given webdriver.
	'''
	@abstractmethod
	def exec(self, webdriver):
		pass
