from . import runner


# Spawn selenium webdriver and run axe based on configs.
def run(configs):
	(runner.Runner(configs)).exec()