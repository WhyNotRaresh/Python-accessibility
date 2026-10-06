from . import abstract_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


'''
Command used to click on an element identified by a CSS selector.
'''
class ClickCommand(abstract_command.AbstractCommand):


	'''
	Command constructor.

	Store the CSS selector of the element to click.
	'''
	def __init__(self, options):
		self.selector = options['selector']


	'''
	Execute the command.

	Wait for the element to be clickable, then click it.
	'''
	def exec(self, webdriver):
		element = WebDriverWait(webdriver, 5).until(
			expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, self.selector))
		)

		webdriver.execute_script('arguments[0].click();', element)


