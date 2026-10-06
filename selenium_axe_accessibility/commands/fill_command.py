from . import abstract_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


'''
Command used to fill a form element with a specified value.
'''
class FillCommand(abstract_command.AbstractCommand):


	'''
	Command constructor.

	Store the CSS selector of the form element and the value to fill it with.
	'''
	def __init__(self, options):
		self.selector = options['selector']
		self.value = options['value']
		self.timeout = options.get('timeout', 60)


	'''
	Execute the command.

	Wait for the element to be present, clear it, then fill it with the given value.
	'''
	def exec(self, webdriver):
		element = WebDriverWait(webdriver, self.timeout).until(
			expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, self.selector))
		)
		element.clear()
		element.send_keys(self.value)
