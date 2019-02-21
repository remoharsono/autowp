import os
from autowp.apps.shared.base.exceptions import ConfigError
from autowp.apps.shared.config.data import Config

class Parser(object):

	def __init__(self, conf: Config):
		mongo_host = os.getenv('MONGO_HOST')
		mongo_dbname = os.getenv('MONGO_DBNAME')
		mongo_conn_timeout = os.getenv('MONGO_CONNECT_TIMEOUT')
		mongo_socket_timeout = os.getenv('MONGO_SOCKET_TIMEOUT')
		mongo_server_selection_timeout = os.getenv('MONGO_SERVER_SELECTION_TIMEOUT')
		salt = os.getenv('SALT')

		# cannot continue without salt key
		if not salt:
			raise ConfigError('SALT', 'You should set your salt key')

		# cannot continue without mongo
		if not mongo_host:
			raise ConfigError('MONGO_HOST', 'You should setup mongo host uri before using this application.')

		# rewrite value connection timeout
		if not mongo_conn_timeout:
			mongo_conn_timeout = 5000 

		# rewrite value socket timeout
		if not mongo_socket_timeout:
			mongo_socket_timeout = 1000

		if not mongo_server_selection_timeout:
			mongo_server_selection_timeout = 15000

		self.config = conf(
			mongo_host=mongo_host, 
			mongo_dbname=mongo_dbname,
			salt=salt,
			mongo_connect_timeout=mongo_conn_timeout,
			mongo_socket_timeout=mongo_socket_timeout,
			mongo_server_selection_timeout=mongo_server_selection_timeout,
		)
