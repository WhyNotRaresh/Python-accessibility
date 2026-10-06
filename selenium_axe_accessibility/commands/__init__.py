from . import abstract_command, goto_command, run_axe_command, click_command, fill_command, wait_for_url_command, submit_command
import importlib


'''
Registry of built-in commands.

Maps command names to their 'module.ClassName' string.
Use register_command() to add new commands at runtime.
'''
_command_registry: dict[str, str] = {
	'go_to':            'goto_command.GoToCommand',
	'run_axe':          'run_axe_command.RunAxeCommand',
	'click':            'click_command.ClickCommand',
	'fill':             'fill_command.FillCommand',
	'wait_for_url':     'wait_for_url_command.WaitForUrlCommand',
	'submit':           'submit_command.SubmitCommand',
}


'''
Register a new command in the command registry.

name       -- the command name used in config dicts
class_path -- 'module.ClassName' string, resolved relative to this package,
              or a fully qualified path for commands defined outside the package.

Example:
    register_command('my_command', 'my_command.MyCommand')
'''
def register_command(name: str, class_path: str):
	_command_registry[name] = class_path


'''
Instantiate and return the appropriate command class for the given options.

The 'command' key in command_options is looked up in the registry.
If not found, the value is treated as a literal 'module.ClassName' string,
allowing custom commands to be used without registering them.
'''
def command_factory(command_options: dict) -> abstract_command.AbstractCommand:
	command_name = command_options.get('command')

	class_path = _command_registry.get(command_name, command_name)
	module_name, class_name = class_path.rsplit('.', 1)

	module = importlib.import_module(f'.{module_name}', package=__package__)
	cls = getattr(module, class_name)
	return cls(command_options)
