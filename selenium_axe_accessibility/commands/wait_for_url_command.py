from . import abstract_command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


'''
Command used to wait until the current URL matches a given prefix.
'''
class WaitForUrlCommand(abstract_command.AbstractCommand):


	'''
	Command constructor.

	Store the URL prefix to wait for.
	'''
	def __init__(self, options):
		self.url = options['url'] + '*'
		self.timeout = options.get('timeout', 60)


	'''
	Execute the command.

	Wait until the current URL matches the prefix.
	'''
	def exec(self, webdriver):
		WebDriverWait(webdriver, self.timeout).until(
			expected_conditions.url_matches(self.url)
		)
