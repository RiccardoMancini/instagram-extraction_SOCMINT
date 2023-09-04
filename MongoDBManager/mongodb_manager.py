import logging
from Settings.settings_manager import SettingsManager
from pymongo import MongoClient
import bcrypt


class DBConnection:
    def __init__(self, database_name: str = 'socmint'):
        self.__logger__()
        self.logger.info('DBConnection init')
        setting_manager = SettingsManager()
        self.client = MongoClient(setting_manager.get_db_URI())
        self.db = self.client[database_name]

    def get_settings(self):
        self.settings = self.db['settings']
        settings = self.settings.find_one()
        return settings

    def get_user_settings(self, username: str = 'marcomameli01'):
        self.user_settings = self.db['users']
        self.user = self.user_settings.find_one({'username': username})
        return self.user

    def __logger__(self):
        # Logging configuration
        # Create logger for Instagram Service
        self.logger = logging.getLogger('SOCMINT.DBManager')
        self.logger.setLevel(logging.DEBUG)
        # File handler logger
        fh = logging.FileHandler('./logging/DBManager.log')
        fh.setLevel(logging.DEBUG)
        # Console handler logger
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # logging formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add handler to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
