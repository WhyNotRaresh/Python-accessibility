from datetime import date
from os import path, makedirs
from . import abstract_writer
import csv


'''
CSV writer class.

Write violations to a CVS file. The resulting file will have the following columns:
 - URL -> the url where the violation was detected;
 - Name -> the name of the violation;
 - Impact -> the Axe impact level of the violation;
 - Count -> how many times the violation was detected on the page;
 - HTML Target -> a list of html nodes (separated by ';;') where the violation was detected.
'''
class CSVWriter(abstract_writer.AbstractWriter):


	'''
	Class constructor.
	'''
	def __init__(self, directory = None, username = None, resolution = None):
		self.file_name = self.create_file_name(directory, username, resolution)


	'''
	Dunder file opening method.
	'''
	def __enter__(self):
		self.file = open(self.file_name, 'w')
		self.file.write('sep=,\n')

		self.csv_writer = csv.writer(self.file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		self.csv_writer.writerow(['URL', 'Name', 'Impact', 'Count', 'HTML Target'])

		return self.csv_writer


	'''
	Dunder file closing method.
	'''
	def __exit__(self, exc_type, exc_value, traceback):
		if self.file:
			self.file.close()


	'''
	Creates result CSV file name based on the used configs.
	'''
	def create_file_name(self, directory = None, username = None, resolution = None):
		if directory is not None:
			if not path.isabs(directory):
				directory = path.abspath(directory)

			if directory[-1] != '/':
				directory = directory + '/'

			if not path.exists(directory):
				makedirs(directory)
		else:
			directory = ''
		
		today = date.today().strftime("%b-%d-%Y")
		file_name = 'accessibility-' + today

		if username is not None:
			file_name = file_name + '-' + username

		if resolution is not None:
			file_name = file_name + '-' + resolution.replace(',', 'x')

		return path.join(directory, file_name + '.csv')


	'''
	Register the violation in the CSV file.
	'''
	def register_violation(self, violation, url):
		target_nodes = []
		count = 0

		for target_node in violation['nodes']:
			target_nodes.append(target_node['html'].replace('\n', ''))
			count += 1

		self.csv_writer.writerow([
			url,
			violation['help'],
			violation['impact'],
			count,
			" ;; ".join(target_nodes)
		])
	