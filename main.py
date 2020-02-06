import logging
import logging.config
import time
import argparse
import sys
import cProfile
import re


class Main():
    def __init__(self):
        self.config = self._parse_args()
        self.logger = self._setup_logging()
        self.timer = self._setup_timing()

    def _parse_args(self):
        '''
        Parses command line arguments, new ones are added here

        returns configuration
        '''
        parser = argparse.ArgumentParser(description='Small script to do X')
        parser.add_argument('-l',
                            '--log_config',
                            default="log_config",
                            help="Use custom logging configuration file")
        parser.add_argument('-p',
                            '--profile',
                            dest='profile',
                            default=False,
                            const=True,
                            action='store_const',
                            help="Profile the user code")
        parser.add_argument('-t',
                            '--test',
                            dest='test',
                            default=False,
                            const=True,
                            action='store_const',
                            help="Run unit tests instead of the program")
        return parser.parse_args()

    def _setup_logging(self):
        '''
        Attempts to load a logging config from disk
        if it is not found a standard one is created

        returns a logger
        '''
        try:
            logging.config.fileConfig(self.config.log_config)
        except Exception as E:
            tempLogger = logging.getLogger(__name__)
            tempLogger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            error_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            handler.setFormatter(logging.Formatter(standard_format))
            tempLogger.addHandler(handler)
            error = "Using default logger. " + str(E)
            tempLogger.warn(error)

        logger = logging.getLogger(__name__)
        logger.info("Logger set up")
        return logger

    def _setup_timing(self):
        return time.time()

    def start_timer(self):
        ''' Reset the timer '''
        self.timer = time.time()

    def stop_timer(self):
        '''
        Reset the timer
        returns the time between the current call and previous call,
        or the previous call to start_timer()
        '''
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
            cProfile.runctx('self.user_main()',
                            globals(),
                            locals(),
                            sort='tottime')
        else:
            self.user_main()

    def user_main(self):
        '''
        User code goes here
        '''
        x = 0
        for i in range(100):
            x = x + i
            print(x)


if __name__ == "__main__":
    app = Main()
    app.run()
