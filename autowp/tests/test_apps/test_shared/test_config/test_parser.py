import unittest
from unittest import mock

from autowp.apps.shared.base.exceptions import ConfigError
from autowp.apps.shared.config.parser import Parser
from autowp.apps.shared.config.data import Config

class TestConfigParser(unittest.TestCase):

	@mock.patch('autowp.apps.shared.config.parser.os')
	def test_parser_success(self, mock_os):
		def side_effect(value):
			envs = {
				'MONGO_HOST': 'test_host', 
				'MONGO_DBNAME': 'test_dbname', 
				'MONGO_CONNECT_TIMEOUT': None,
				'MONGO_SOCKET_TIMEOUT': None,
				'MONGO_SERVER_SELECTION_TIMEOUT': None,
				'SALT': 'test_salt' 
			}

			return envs[value]

		mock_os.getenv.side_effect = side_effect
		parser = Parser(Config)
		self.assertEqual('test_host', parser.config.mongo_host)
		self.assertEqual('test_dbname', parser.config.mongo_dbname)

		mock_os.getenv.assert_any_call('MONGO_HOST')	
		mock_os.getenv.assert_any_call('MONGO_DBNAME')	

	@mock.patch('autowp.apps.shared.config.parser.os')
	def test_parser_none(self, mock_os):
		def side_effect(value):
			envs = {
				'MONGO_HOST': None, 
				'MONGO_DBNAME': None, 
				'MONGO_CONNECT_TIMEOUT': None,
				'MONGO_SOCKET_TIMEOUT': None,
				'MONGO_SERVER_SELECTION_TIMEOUT': None,
				'SALT': None
			}

			return envs[value]

		mock_os.getenv.side_effect = side_effect
		with self.assertRaises(ConfigError):
			parser = Parser(Config)
