import asyncio
import dataset
from stuf import stuf
import random
import sqlalchemy

class Database(object):
    def __init__(self, db):
        self.db = db

        self.guilds = self.db['guilds']

        self.prepareLog()
        self.preparePlayer()
        self.prepareInventory()
        self.prepareItems()
        self.prepareLocations()
        self.prepareActions()
        self.prepareConditions()
        self.prepareResults()

    def prepareLog(self):
        try:
            self.log = self.db.load_table('log')
        except sqlalchemy.exc.NoSuchTableError:
            self.log = self.db.create_table('log')

            self.log.create_column('userId', sqlalchemy.INT)
            self.log.create_column('action', sqlalchemy.TEXT)
            self.log.create_column('result', sqlalchemy.INT)
            self.log.create_column('timestamp', sqlalchemy.DATETIME)

            self.log = self.db.load_table('log')

    def preparePlayer(self):
        try:
            self.player = self.db.load_table('players')
        except sqlalchemy.exc.NoSuchTableError:
            self.player = self.db.create_table('players')

            self.player.create_column('userId', sqlalchemy.INT)
            self.player.create_column('deaths', sqlalchemy.INT)
            self.player.create_column('wins', sqlalchemy.INT)

            self.player.create_index(['userId'])

            self.player = self.db.load_table('players')

    def prepareInventory(self):
        try:
            self.inventory = self.db.load_table('inventory')
        except sqlalchemy.exc.NoSuchTableError:
            self.inventory = self.db.create_table('inventory')

            self.player.create_column('userId', sqlalchemy.INT)
            self.player.create_column('itemId', sqlalchemy.INT)
            self.player.create_column('count', sqlalchemy.INT)
            self.player.create_column('itemType', sqlalchemy.INT)

            self.player.create_index(['userId', 'itemType'])

            self.inventory = self.db.load_table('inventory')

    def prepareItems(self):
        try:
            self.items = self.db.load_table('items')
        except sqlalchemy.exc.NoSuchTableError:
            self.items = self.db.create_table('items')

            self.items.create_column('name', sqlalchemy.TEXT)
            self.items.create_column('type', sqlalchemy.INT)

            self.items.create_index(['name'])

            self.items = self.db.load_table('items')

    def prepareLocations(self):
        try:
            self.locations = self.db.load_table('locations')
        except sqlalchemy.exc.NoSuchTableError:
            self.locations = self.db.create_table('locations')

            self.locations = self.db.load_table('locations')

    def prepareActions(self):
        try:
            self.actions = self.db.load_table('actions')
        except sqlalchemy.exc.NoSuchTableError:
            self.actions = self.db.create_table('actions')

            self.actions = self.db.load_table('actions')

    def prepareConditions(self):
        try:
            self.conditions = self.db.load_table('conditions')
        except sqlalchemy.exc.NoSuchTableError:
            self.conditions = self.db.create_table('conditions')

            self.conditions = self.db.load_table('conditions')

    def prepareResults(self):
        try:
            self.results = self.db.load_table('results')
        except sqlalchemy.exc.NoSuchTableError:
            self.results = self.db.create_table('results')

            self.results = self.db.load_table('results')
