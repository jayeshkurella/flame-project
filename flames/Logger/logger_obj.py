import logging
import sys
import datetime
import os

date = datetime.date.today()

class Logger:
    def __init__(self):
        try:
            self.create_logs_directory()
            log_file = os.path.join("Logger/user_log_files", f"log_{date}.log")
            dev_log_file = os.path.join("Logger/dev_log_files", f"devlog_{date}.log")
            self.logger = self._setup_logger('SMART_logger', log_file, level=logging.INFO)
            self.dev_logger = self._setup_logger('SMARTdev_logger', dev_log_file, level=logging.DEBUG)
        except Exception as e:
            print(f"Failed to initialize Logger: {e}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def create_logs_directory():
        this_folder = os.path.dirname(__file__)
        user_log_folder = os.path.join(this_folder, "Logger/user_log_files")
        dev_log_folder = os.path.join(this_folder, "Logger/dev_log_files")

        for folder in [user_log_folder, dev_log_folder]:
            try:
                if not os.path.exists(folder):
                    print(f"Creating log folder: {folder}")
                    os.makedirs(folder)
            except Exception as e:
                print(f"Failed to create directory {folder}: {e}", file=sys.stderr)
                raise

    @staticmethod
    def _setup_logger(name, log_file, level=logging.INFO):
        """To setup as many loggers as you want"""
        try:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
            handler.setFormatter(formatter)

            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.addHandler(handler)
            if level == logging.INFO:
                logger.addHandler(logging.StreamHandler(sys.stdout))

            logger.debug("logging started")

            return logger
        except Exception as e:
            print(f"Failed to setup logger {name}: {e}", file=sys.stderr)
            raise

    def debug(self, msg):
        self.logger.debug(msg)
        self.dev_logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)
        self.dev_logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)
        self.dev_logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
        self.dev_logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
        self.dev_logger.critical(msg)
