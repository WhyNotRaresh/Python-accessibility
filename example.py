import selenium_axe_accessibility
import json	


### RUN EXAMPLE ###


if __name__ == '__main__':

	# Loading configs.
	configs = open('configs.json')
	configs_data = json.load(configs)

	selenium_axe_accessibility.run(configs_data)
