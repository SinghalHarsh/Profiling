"""Configuration for the package is handled in this wrapper for confuse."""
import os
import yaml

class Config(object):
    
    config = None
    """The confuse.Configuration object."""

    def __init__(self):
        
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "config_default.yaml")) as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
        
    def set(self, key, value):
        self.config[key] = value


config = Config()
