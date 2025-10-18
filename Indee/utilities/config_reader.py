import configparser
import os


class ConfigReader:
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
        self.config.read(config_path)
    
    def get_pin(self):
        return self.config.get('credentials', 'pin')
    
    def get_url(self):
        return self.config.get('platform', 'url')


_config = None

def get_config():
    global _config
    if _config is None:
        _config = ConfigReader()
    return _config

