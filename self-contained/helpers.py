import yaml
import sys

class Config(object):

    config_path = "data/test_config.yml"

    def __init__(self, path=config_path):
        configfile = yaml.load(open(path, newline=''))

        self.tokens = configfile['tokens']
