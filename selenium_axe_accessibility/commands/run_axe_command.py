from . import abstract_command
from axe_selenium_python import Axe


'''
Run the Axe accessibility tool on the current page.
'''
class RunAxeCommand(abstract_command.AbstractCommand):


	'''
	Command constructor.
	'''
	def __init__(self, options):
		pass


	'''
	Execute the command.

	Run the axe webtools tool on the page.
	'''
	def exec(self, webdriver):
		axe_webtools = Axe(webdriver)
		axe_webtools.inject()
		return axe_webtools.run()

