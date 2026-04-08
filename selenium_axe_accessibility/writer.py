import time
import csv


# Creates result CSV file name based on the used configs.
def create_file_name(configs_data):
	from datetime import date
	from os import path, makedirs

	if 'dir' in configs_data.keys():
		directory = configs_data['dir']

		if not path.isabs(directory):
			directory = path.abspath(directory)

		if not path.exists(directory):
			makedirs(directory)
	
	today = date.today().strftime("%b-%d-%Y")

	file_name = 'accessibility-' + today

	if configs_data['env'] in ['local', 'acc', 'prod']:
		file_name = file_name + '-' + configs_data['env']

	if configs_data['login']:
		file_name = file_name + '-' + configs_data['login']['username']

	if 'resolution' in configs_data.keys():
		file_name = file_name + '-' + configs_data['resolution'].replace(',', 'x')

	return path.join(directory, file_name + '.csv')


# Writes violation result to the CSV file.
def wirte_result(csv_writer, violation, url):

	target_nodes = []
	count = 0

	for target_node in violation['nodes']:
		target_nodes.append(target_node['html'].replace('\n', ''))
		count += 1

	csv_writer.writerow([
		url,
		violation['help'],
		violation['impact'],
		count,
		" ;; ".join(target_nodes)
	])



