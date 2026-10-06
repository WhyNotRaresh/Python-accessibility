from . import abstract_command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


'''
Command used to submit the form that a given element belongs to.
'''
class SubmitCommand(abstract_command.AbstractCommand):


	'''
	Command constructor.

	Store the CSS selector of the element whose form will be submitted.
	'''
	def __init__(self, options):
		self.selector = options['selector']


	'''
	Execute the command.

	Wait for the element to be present, then submit its form.
	'''
	def exec(self, webdriver):
		element = WebDriverWait(webdriver, 5).until(
			expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.selector))
		)
		element.submit()
