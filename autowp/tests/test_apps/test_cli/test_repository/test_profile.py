import unittest
from unittest import mock

from autowp.core.shared.exceptions import StorageError, VarTypeError
from autowp.core.profile.entity import Profile, Password
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.shared.config import config
from autowp.apps.shared.security.hasher import Sha256Hasher

class ProfileRepoTestCase(unittest.TestCase):

	def tearDown(self):
		"""Will delete all documents after of each tests"""
		repo = ProfileRepository(config())
		coll = repo.build_mongo_coll(repo.COLLNAME)
		coll.delete_many({})

	def test_create_success(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)

		repo = ProfileRepository(config())
		self.assertTrue(repo.create(profile))

	@mock.patch('autowp.apps.shared.base.repository.pymongo.collection.Collection.insert_one')	
	def test_create_failed(self, mock_insert):
		mock_insert.return_value = False
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)

		repo = ProfileRepository(config())
		self.assertFalse(repo.create(profile))

	def test_create_invalid_profile(self):
		with self.assertRaises(VarTypeError):
			repo = ProfileRepository(config())
			repo.create('testing')

	@mock.patch('autowp.apps.shared.config.parser.os')
	def test_connection_lost(self, mock_os):
		def side_effect(value):
			envs = {
				'MONGO_HOST': 'mongodb://localhost:9000/autowp_test', 
				'MONGO_DBNAME': 'test_dbname', 
				'MONGO_CONNECT_TIMEOUT': 500,
				'MONGO_SOCKET_TIMEOUT': 100,
				'MONGO_SERVER_SELECTION_TIMEOUT': None
			}

			return envs[value]

		mock_os.getenv.side_effect = side_effect

		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)

		with self.assertRaises(StorageError):
			repo = ProfileRepository(config())
			repo.create(profile)
