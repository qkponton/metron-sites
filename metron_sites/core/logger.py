import logging
import os
from logging.handlers import RotatingFileHandler

from metron_sites.core.singleton import Singleton


class ApiLogger(metaclass=Singleton):

    def __init__(self):
        """
        """
        logger = logging.getLogger()
        log_directory = os.environ.get('LOG_DIRECTORY', '.')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s')

        level = os.environ.get('LOG_LEVEL', logging.INFO)
        logger.setLevel(level)

        file_handler = RotatingFileHandler(os.path.join(log_directory, 'backend.log'), maxBytes=1000000000, backupCount=3)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    @staticmethod
    def get_logger():
        """
        :return: logging.Logger
        """
        return logging.getLogger('Metron Sites')
