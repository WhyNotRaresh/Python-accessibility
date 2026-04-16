'''
Abstract result writer.
'''
class AbstractWriter:

	'''
	Class constructor.
	'''
	def __init__(self, directory:str = None, username:str = None, resolution:str = None):
		pass


	'''
	Dunder file opening method.
	'''
	def __enter__(self):
		pass


	'''
	Dunder file closing method.
	'''
	def __exit__(self, exc_type, exc_value, traceback):
		pass


	'''
	Register the violation in the CSV file.
	'''
	def register_violation(self, violation:list, url:str):
		pass
