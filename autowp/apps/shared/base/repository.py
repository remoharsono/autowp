import pymongo
from autowp.apps.shared.config.data import Config

class BaseRepository(object):

	def __init__(self, config: Config):
		"""Build mongo connection and database object"""
		self.mongo = pymongo.MongoClient(
			host=config.mongo_host, 
			socketTimeoutMS=config.mongo_socket_timeout,
			connectTimeoutMS=config.mongo_connect_timeout,
			serverSelectionTimeoutMS=config.mongo_server_selection_timeout
		)

		self.db = self.mongo[config.mongo_dbname]

	def build_mongo_coll(self, name: str) -> pymongo.collection.Collection:
		"""Build mongo collection object"""
		return self.db[name]
