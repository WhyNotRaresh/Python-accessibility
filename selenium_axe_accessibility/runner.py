from selenium_axe_accessibility.writers.csv_writer import CSVWriter
from selenium_axe_accessibility.writers.abstract_writer import AbstractWriter
from selenium_axe_accessibility.commands import command_factory
from . import config
from selenium import webdriver
import time


class Runner:


	'''
	Class constructor.
	'''
	def __init__(self, configs):
		self.config = config.Config(configs)
		self.host = configs['env']
		self.driver = None


	'''
	Create complete URL from a given path.
	'''
	def form_url(self, path):
		return self.host + self.config.get('path_prefix') + path;


	'''
	Spawn webdriver.
	'''
	def spawn(self):
		opts = webdriver.ChromeOptions()
		opts.timeouts = {
			'script': 300000, 
			'implicit': 100
		}
		opts.add_argument('--window-size=' + self.config.get_resolution())

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
		for command_options in self.config.get_login_commands():
			command_factory(command_options).exec(self.driver)


	'''
	Execute accesibility run.
	'''
	def exec(self, writer:AbstractWriter = None):
		self.spawn()

		login_commands = self.config.get_login_commands()
		# Logging in with the user.
		if login_commands:
			try:
				self.login()
			except:
				print('Failed to login in.')

				login = self.config.get('login')
				if login.get('continue_on_fail'):
					self.config.set('login', False)
					print('Continuing the process as an anonymous user.')
				else:
					raise Exception('Stopped execution because of failed login.') 

		if not writer:
		 	writer = CSVWriter(self.config.get('dir'), self.config.get_username(), self.config.get_resolution())

		with writer:
			for command in self.config.get('commands'):
				command = command_factory(command)
				results = command.exec(self.driver)

				if results is not None:
					for violation in results['violations']:
						writer.register_violation(violation, self.driver.current_url)

		self.despawn()
