import logging
import sys
import datetime
import os

date = datetime.date.today()


class Logger:
    def __init__(self):
        self.create_logs_directory()

        self.logger = self._setup_logger('SMART_logger', f"Logger/user_log_files/log_{date}.log", level=logging.INFO)
        self.dev_logger = self._setup_logger('SMARTdev_logger', f"Logger/dev_log_files/devlog_{date}.log",
                                             level=logging.DEBUG)

    @classmethod
    def create_logs_directory(cls):
        this_file = __file__
        print(f"This File.. {this_file}")
        this_folder = os.path.split(this_file)[0]

        log_folder = os.path.join(this_folder, "dev_log_files")
        if not os.path.exists(log_folder):
            print("Creating log folder", log_folder)
            os.mkdir(log_folder)
        log_folder = os.path.join(this_folder, "user_log_files")
        if not os.path.exists(log_folder):
            print("Creating log folder", log_folder)
            os.mkdirs(log_folder)

    @staticmethod
    def _setup_logger(name, log_file, level=logging.INFO):
        """To setup as many loggers as you want"""

        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)

        logger = logging.getLogger(name + __name__)
        logger.setLevel(level)
        logger.addHandler(handler)
        if level == logging.INFO:
            logger.addHandler(logging.StreamHandler(sys.stdout))

        logger.debug("logging started")

        return logger

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
