from selenium_axe_accessibility.writers.csv_writer import CSVWriter
from selenium_axe_accessibility.writers.abstract_writer import AbstractWriter
from selenium import webdriver
from axe_selenium_python import Axe
import time


class Runner:


	'''
	Class constructor.
	'''
	def __init__(self, configs):
		self.configs = configs
		self.host = configs['env']
		self.driver = None


	'''
	Create complete URL from a given path.
	'''
	def form_url(self, path):
		return self.host + self.configs['path_prefix'] + path;


	'''
	Spawn webdriver.
	'''
	def spawn(self):
		if 'resolution' in self.configs.keys():
			resolution = self.configs['resolution']
		else:
			resolution = '1920,1080'

		# Selenium self.driver.
		opts = webdriver.ChromeOptions()
		opts.timeouts = {
			'script': 300000, 
			'implicit': 100
		}
		opts.add_argument('--window-size=' + resolution)

		self.driver = webdriver.Chrome(options=opts)

		return self


	'''
	Despawn webdriver.
	'''
	def despawn(self):
		self.driver.close()
		self.drive = None


	'''
	Do login procedure.
	'''
	def login(self):
		from selenium.webdriver.common.by import By
		from selenium.webdriver.support import expected_conditions
		from selenium.webdriver.support.ui import WebDriverWait

		login_data = self.configs['login']

		# Set default values for eulogin login.
		if login_data['is_eulogin']:
			login_data['url'] = '/eulogin'
			login_data['username_field'] = 'input#username'
			login_data['password_field'] = 'input#password'

		# Tuple used to select the username field.
		username_select = (By.CSS_SELECTOR, login_data['username_field'])
		# Tuple used to select the password field.
		password_select = (By.CSS_SELECTOR, login_data['password_field'])

		# Go to the login URL.
		self.driver.get(self.form_url(login_data['url']))

		# Wait for up to 5 seconds for the username field to be present on the page.
		WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located(username_select))
		# Find the element on the page.
		username_input_element = self.driver.find_element(*username_select)
		# Fill the field with the given username.
		username_input_element.send_keys(login_data['username'])

		if login_data['is_eulogin']:
			# An intermediary sumbmit action is needed.
			username_input_element.submit()

			# Wait for up to 5 seconds for the password field to be present on the page after the intermediary submit.
			WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located(password_select))

		# Find the element on the page.
		password_input_element = self.driver.find_element(*password_select)
		# Fill the field with the given password.
		password_input_element.send_keys(login_data['password'])

		if login_data['is_eulogin']:
			# Switch to password login.
			self.driver.find_element(By.ID, 'verif-method-dd-id').click()
			self.driver.find_element(By.ID, 'verif-method-dd-PASSWORD').click()

		# Submit the form.
		password_input_element.submit()

		# Wait for eulogin redirect back to the platform.
		WebDriverWait(self.driver, 5).until(expected_conditions.url_matches(self.host + '*'))


	'''
	Run the axe webtools tool on the page.
	'''
	def run_axe(self, axe_webtools):
		from selenium.webdriver.common.by import By
		from selenium.common.exceptions import NoSuchElementException

		# Remove any unwanted elements from the page.
		if 'remove' in self.configs.keys():
			for css_selector in self.configs['remove']:
				try:
					element = self.driver.find_element(by=By.CSS_SELECTOR, value=css_selector)
					self.driver.execute_script("""
						var element = arguments[0];
						element.parentNode.removeChild(element);
						""", element)
				except NoSuchElementException:
					pass

		axe_webtools.inject()
		return axe_webtools.run()


	'''
	Execute accesibility run.
	'''
	def exec(self, writer:AbstractWriter = None):
		self.spawn()

		# Logging in with the user.
		if self.configs['login']:
			try:
				self.login()
			except:
				print('Failed to login in.')

				if self.configs['login']['continue_on_fail']:
					self.configs['login'] = False
					print('Continuing the process as an anonymous user.')
				else:
					raise Exception('Stopped execution because of failed login.') 

		# Axe tool for accessibility.
		axe_webtools = Axe(self.driver)

		if not writer:
		 	writer = CSVWriter(self.configs['dir'], self.configs['login']['username'], self.configs['resolution'])

		with writer:
			for path in self.configs['paths']:
				url = self.form_url(path)

				try:
					self.driver.get(url)
					time.sleep(1)

					results = self.run_axe(axe_webtools)

					for violation in results['violations']:
						writer.register_violation(violation, url)
				except:
					print('Error occured on url ' + url)

		self.despawn()
