import yaml
import sys
import discord
import atexit

config_path = "data/config.yml"
server_path = "data/servers/"

class Global(object):
    def __init__(self, path=config_path):
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
            self.whitelist = configfile['whitelist']
            self.blacklist = configfile['blacklist']

        except FileNotFoundError:
            print("Sorry, I couldn't find config.yml")
            sys.exit()
        except IOError:
            print("Sorry, I couldn't open config.yml")
            sys.exit()
        except yaml.parser.ParserError:
            print("Sorry, I couldn't parse config.yml")
            sys.exit()


class ServerConfig(object):
    def __init__(self, server: discord.Server, path=server_path):
        self.server = server
        self.path = path + server.id + ".yml"

        try:
            configfile = yaml.load(open(self.path))
        except FileNotFoundError:

            pass
        except IOError:
            pass
        except yaml.parser.ParserError:
            pass

    def create_config(self):
        pass