from . import runner


'''
Run an accessibility audit using the default CSV writer.

Spawns a Chrome WebDriver, executes all configured commands,
and writes violations to a CSV file in the configured output directory.
'''
def run(configs):
	(runner.Runner(configs)).exec()


'''
Run an accessibility audit using a custom writer.

Behaves like run(), but uses the provided writer instance instead of
the default CSV writer. The writer must extend AbstractWriter.
'''
def run_with_writer(configs, writer):
	(runner.Runner(configs)).exec(writer)
