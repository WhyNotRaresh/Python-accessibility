from selenium import webdriver
from axe_selenium_python import Axe
import time
import json
import csv


global configs_data
global host


# Create complete URL from a given path.
def form_url(path):
	return host + configs_data['langcode'] + path;


# Creates result CSV file name based on the used configs.
def create_file_name():
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


# Logs user in.
def do_login(driver):
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support import expected_conditions
	from selenium.webdriver.support.ui import WebDriverWait

	login_data = configs_data['login']

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
	driver.get(form_url(login_data['url']))

	# Wait for up to 5 seconds for the username field to be present on the page.
	WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located(username_select))
	# Find the element on the page.
	username_input_element = driver.find_element(*username_select)
	# Fill the field with the given username.
	username_input_element.send_keys(login_data['username'])

	if login_data['is_eulogin']:
		# An intermediary sumbmit action is needed.
		username_input_element.submit()

		# Wait for up to 5 seconds for the password field to be present on the page after the intermediary submit.
		WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located(password_select))

	# Find the element on the page.
	password_input_element = driver.find_element(*password_select)
	# Fill the field with the given password.
	password_input_element.send_keys(login_data['password'])

	if login_data['is_eulogin']:
		# Switch to password login.
		driver.find_element(By.ID, 'verif-method-dd-id').click()
		driver.find_element(By.ID, 'verif-method-dd-PASSWORD').click()

	# Submit the form.
	password_input_element.submit()

	# Wait for eulogin redirect back to the platform.
	WebDriverWait(driver, 10).until(expected_conditions.url_matches(host + '*'))


# Accept term and conditions.
def accept_cookies(driver):
	from selenium.webdriver.common.by import By

	url = form_url('/')
	driver.get(url)

	time.sleep(0.5)

	accept_button = driver.find_element(by=By.CSS_SELECTOR, value='#cookie-consent-banner a[href="#accept"]')
	accept_button.click()


# Run the axe webtools tool on the page.
def run_axe(axe_webtools, driver):
	from selenium.webdriver.common.by import By
	from selenium.common.exceptions import NoSuchElementException

	# Remove any unwanted elements from the page.
	if 'remove' in configs_data.keys():
		for css_selector in configs_data['remove']:
			try:
				element = driver.find_element(by=By.CSS_SELECTOR, value=css_selector)
				driver.execute_script("""
					var element = arguments[0];
					element.parentNode.removeChild(element);
					""", element)
			except NoSuchElementException:
				pass

	axe_webtools.inject()
	return axe_webtools.run()


### SCRIPT BEGINING ###

if __name__ == '__main__':

	# Loading configs.
	configs = open('configs.json')
	configs_data = json.load(configs)

	if configs_data['env'] == 'prod':
		host = 'https://epale.ec.europa.eu/'
	elif configs_data['env'] == 'acc':
		host = 'https://shared:BasicAuthEU2024@eacea-epale.acc.fpfis.tech.ec.europa.eu/'
	elif configs_data['env'] == 'local':
		host = 'http://localhost:8080/'
	else:
		host = configs_data['env']

	if 'resolution' in configs_data.keys():
		resolution = configs_data['resolution']
	else:
		resolution = '1920,1080'


	# Selenium driver.
	opts = webdriver.ChromeOptions()
	opts.timeouts = {
		'script': 300000, 
		'implicit': 100
	}
	opts.add_argument('--window-size=' + resolution)
	driver = webdriver.Chrome(options=opts)

	# Logging in with the user.
	if configs_data['login']:
		try:
			do_login(driver)
		except:
			print('Failed to login in.')

			if configs_data['login']['continue_on_fail']:
				configs_data['login'] = False
				print('Continuing the process as an anonymous user.')
			else:
				raise Exception('Stopped execution because of failed login.') 

	# Accepting cookies.
	if configs_data['env'] == 'prod' or configs_data['env'] == 'acc':
		accept_cookies(driver)

	# Axe tool for accessibility.
	axe_webtools = Axe(driver)

	with open(create_file_name(), 'w', newline='') as csv_result_file:
		csv_result_file.write('sep=,\n')

		# CSV writer object.
		csv_writer = csv.writer(csv_result_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(['URL', 'Name', 'Impact', 'Count', 'HTML Target'])

		for path in configs_data['paths']:
			url = form_url(path)

			try:
				driver.get(url)
				time.sleep(1)

				results = run_axe(axe_webtools, driver)

				for violation in results['violations']:
					wirte_result(csv_writer, violation, url)
			except:
				print('Error occured on url ' + url)

	driver.close()
