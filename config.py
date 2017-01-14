import yaml
import sys
import discord
import atexit
from pubsub import pub

config_path = "data/config.yml"
server_path = "data/servers/"

class Global(object):
    def __init__(self, path=config_path):
        self.load_yaml(path)

    def load_yaml(self, path):
        try:
            configfile = yaml.load(open(path, newline=''))

            if "token" in configfile:
                self.token = configfile['token']
            else:
                print("Um, Mistress, my configuration file doesn't have a token.\n"
                      "I don't know what to do!")
                sys.exit()
            self.owners = configfile['owners']
            if "owners" not in configfile:
                print("Mistress, there aren't any owner ids in my configuration.\n"
                      "I won't know who you are!")
            self.notify = configfile['notify'] if "notify" in configfile else True
            self.favored = configfile['favored'] if "favored" in configfile else {}
            self.whitelist = configfile['whitelist']
            self.blacklist = configfile['blacklist']
            self.module_whitelist = configfile['module_whitelist']
            if 'Permissions' not in self.module_whitelist:
                self.module_whitelist.append("Permissions")
            self.backstory = configfile['backstory']
            self.backstory['timer'] = configfile['backstory']['timer'] if (
                'timer' in self.backstory) else 20
            self.files = configfile['files']
            if "files" not in configfile:
                print("Mistress, I don't know where any of my files are.\n"
                      "Many parts of me won't work!")
                sys.exit()
            else:
                if "database" not in self.files:
                    print("Mistress, I can't find my database!")
                    sys.exit()
                if "log" not in self.files:
                    print("Mistress, I can't find my logfile!")
                    sys.exit()

        except FileNotFoundError:
            print("Sorry, I couldn't find config.yml")
            sys.exit()
        except IOError:
            print("Sorry, I couldn't open config.yml")
            sys.exit()
        except yaml.parser.ParserError:
            print("Sorry, I couldn't parse config.yml")
            sys.exit()
