import logging, logging.config
import time
import argparse
import sys
import ConfigParser
import cProfile
import re

class Main():
	def __init__(self):
		self._parse_args()
		self._setup_logging()
		self._setup_timing()

	def _parse_args(self):
		# Parses command line arguments, new ones are added here
		parser = argparse.ArgumentParser(description='Small script to do X')
		parser.add_argument('-l', '--log_config', default="log_config", help="Use custom logging configuration file")
		parser.add_argument('-p', '--profile', dest='profile', default=False, const=True, action='store_const', help="Profile the user code")
		parser.add_argument('-t', '--test', dest='test', default=False, const=True, action='store_const', help="Run unit tests instead of running the program")
		self.config = parser.parse_args()

	def _setup_logging(self):
		# Attempts to load a logging config from disk, if it is not found a standard one is created
		try:
			logging.config.fileConfig(self.config.log_config)
		except Exception as E:
			tempLogger = logging.getLogger(__name__)
			tempLogger.setLevel(logging.DEBUG)
			handler = logging.StreamHandler()
			handler.setLevel(logging.DEBUG)
			handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
			tempLogger.addHandler(handler)
			tempLogger.warn("Unable to load logging configuration, using defaults. Error was: " + str(E))

		self.logger = logging.getLogger(__name__)
		self.logger.info("Logger set up")

	def _setup_timing(self):
		self.timer = time.time()

	def start_timer(self):
		''' Reset the timer '''
		self.timer = time.time()

	def stop_timer(self):
		''' Reset the timer, and return the time between the current call and previous call, or the previous call to start_timer() '''
		difference = time.time() - self.timer
		self.timer = time.time()
		return difference

	def run(self):
		# Calls the user_main method to run the script
		if self.config.test:
			try:
				import our_tests
				our_tests.run()
			except ImportError as E:
				self.logger.critical("Unable to run tests " + str(E))
		elif self.config.profile:
			cProfile.runctx('self.user_main()', globals(), locals(), sort='tottime')
		else:
			self.user_main()

	def user_main(self):
		#User code goes here
		x = 0
		for i in range(100):
			x = x + i
			print x

if __name__ == "__main__":
	app = Main()
	app.run()