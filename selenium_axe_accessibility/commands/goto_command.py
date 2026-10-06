from . import abstract_command
from selenium.webdriver.support.ui import WebDriverWait


'''
Command used to access a specific URL.
'''
class GoToCommand(abstract_command.AbstractCommand):


	'''
	Command constructor.

	Store the URL destination.
	'''
	def __init__(self, options):
		self.url = options['url']


	'''
	Execute the command.

	Go to the destination URL.
	'''
	def exec(self, webdriver):
		webdriver.get(self.url)
		WebDriverWait(webdriver, 1)
