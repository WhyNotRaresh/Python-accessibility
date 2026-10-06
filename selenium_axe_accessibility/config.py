
'''
Holds and prepares the running configuration.

On construction, all command lists (main and login) are formatted:
paths are resolved to full URLs and string shorthands are expanded
into their equivalent command dicts.
'''
class Config:

	'''
	Class constructor.

	Store the raw config dict and format all command lists.
	'''
	def __init__(self, configs):
		self.configs = configs
		self.format_commands()
		self.format_login_commands()


	'''
	Return the configured browser resolution.

	Defaults to 1920,1080 if not specified.
	'''
	def get_resolution(self):
		if 'resolution' not in self.configs.keys():
			self.configs['resolution'] = '1920,1080'

		return self.configs['resolution']


	'''
	Return the formatted list of login commands, or None if login is disabled.
	'''
	def get_login_commands(self):
		if not self.configs.get('login'):
			return None
		return self.configs['login'].get('commands', [])


	'''
	Return the configured username, or None if login is disabled.
	'''
	def get_username(self):
		if not self.configs.get('login'):
			return None

		return self.configs['login'].get('username')


	'''
	Return the value of a config key, or None if the key is not present.
	'''
	def get(self, config_name):
		if config_name in self.configs:
			return self.configs[config_name]

		return None


	'''
	Set a config value.
	'''
	def set(self, config_name, value):
		self.configs[config_name] = value


	'''
	Create a complete URL by joining the base environment URL, the path prefix, and the given path.
	'''
	def form_url(self, path):
		return self.configs['env'] + self.configs['path_prefix'] + path;


	'''
	Format the login command list in place.

	Does nothing if login is disabled.
	'''
	def format_login_commands(self):
		login = self.configs.get('login')
		if not login:
			return

		login['commands'] = self.format_command_list(login.get('commands', []))


	'''
	Format the main command list in place.
	'''
	def format_commands(self):
		self.configs['commands'] = self.format_command_list(self.configs.get('commands', []))


	'''
	Normalise a list of commands.

	String entries are expanded into a go_to + run_axe pair.
	Dict entries that contain a 'path' key have their URL resolved.
	'''
	def format_command_list(self, command_list: list):
		formatted_commands = []

		for command in command_list:
			if type(command) is str:
				# A simple string translates to a GoTo command and a RunAxe command.
				goto_command = {
					'command': 'go_to',
					'path': command
				}
				goto_command['url'] = self.form_url(goto_command['path'])
				formatted_commands.append(goto_command)

				run_axe_command = {
					'command': 'run_axe'
				}
				formatted_commands.append(run_axe_command)

				continue
			elif 'path' in command:
					command['url'] = self.form_url(command['path'])

			formatted_commands.append(command)

		return formatted_commands


