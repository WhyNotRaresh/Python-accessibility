from . import abstract_command, goto_command, run_axe_command, click_command, fill_command, wait_for_url_command, submit_command
from enum import Enum
import importlib


'''
Registry of built-in commands.

Each entry maps a command name to its 'module.ClassName' string.
To add a new built-in command, append an entry here — no other changes are needed.
'''
class DefaultCommands(Enum):
	go_to = 'goto_command.GoToCommand'
	run_axe = 'run_axe_command.RunAxeCommand'
	click = 'click_command.ClickCommand'
	fill = 'fill_command.FillCommand'
	wait_for_url = 'wait_for_url_command.WaitForUrlCommand'
	submit = 'submit_command.SubmitCommand'
	wait_for_element = 'wait_for_element_command.WaitForElementCommand'


'''
Instantiate and return the appropriate command class for the given options.

The 'command' key in command_options is looked up in DefaultCommands.
If not found, it is treated as a literal 'module.ClassName' string,
allowing custom commands to be used without modifying the registry.
'''
def command_factory(command_options: dict) -> abstract_command.AbstractCommand:
	command_name = command_options.get('command')

	# Resolve 'module.ClassName' from the enum registry, or use the name directly.
	try:
		class_path = DefaultCommands[command_name].value
	except KeyError:
		class_path = command_name
	module_name, class_name = class_path.rsplit('.', 1)

	module = importlib.import_module(f'.{module_name}', package=__package__)
	cls = getattr(module, class_name)
	return cls(command_options)
	