import unittest
from bson.objectid import ObjectId

from autowp.core.shared.exceptions import StorageError
from autowp.core.shared.entity import State
from autowp.core.profile.entity import Profile, Password
from autowp.core.security.entity import Session
from autowp.apps.shared.config import config
from autowp.apps.shared.security.hasher import Sha256Hasher
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.cli.repository.security import SecurityRepository
from autowp.apps.cli.adapter.profile.register import RegisterAdapter
from autowp.apps.cli.adapter.security.login import LoginAdapter
from autowp.apps.cli.adapter.security.logout import LogoutAdapter 

class LogoutAdapterTestCase(unittest.TestCase):
	
	def tearDown(self):
		"""Will delete all documents after of each tests"""
		repo = ProfileRepository(config())
		coll = repo.build_mongo_coll(repo.COLLNAME)
		coll.delete_many({})

	def test_logout_success(self):
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)
		profile = adapter.register('test_name', 'test_password')
		self.assertIsInstance(profile, Profile)

		sec_repo = SecurityRepository(config())
		sec_adapter = LoginAdapter(repo, sec_repo, config())
		session = sec_adapter.login(profile.name, 'test_password')
		self.assertIsInstance(session, Session)
		self.assertTrue(sec_repo.is_exist())

		logout_adapter = LogoutAdapter(sec_repo, repo)
		logout_adapter.logout()
		self.assertFalse(sec_repo.is_exist())

	def test_logout_no_session(self):
		repo = ProfileRepository(config())
		sec_repo = SecurityRepository(config())

		logout_adapter = LogoutAdapter(sec_repo, repo)
		logout_adapter.logout()
		self.assertFalse(sec_repo.is_exist())
