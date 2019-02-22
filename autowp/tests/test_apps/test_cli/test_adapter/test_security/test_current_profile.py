import unittest
from bson.objectid import ObjectId

from autowp.core.shared.entity import State
from autowp.core.profile.entity import Profile, Password
from autowp.core.security.entity import Session
from autowp.core.security.usecase.login import LoginUseCase
from autowp.apps.shared.config import config
from autowp.apps.shared.security.hasher import Sha256Hasher
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.cli.repository.security import SecurityRepository
from autowp.apps.cli.adapter.profile.register import RegisterAdapter
from autowp.apps.cli.adapter.security.login import LoginAdapter
from autowp.apps.cli.adapter.security.current_profile import CurrentProfileAdapter

class CurrentProfileAdapterTestCase(unittest.TestCase):
	
	def tearDown(self):
		"""Will delete all documents after of each tests"""
		repo = ProfileRepository(config())
		coll = repo.build_mongo_coll(repo.COLLNAME)
		coll.delete_many({})

		repo_sec = SecurityRepository(config())
		coll_sec = repo_sec.build_mongo_coll(repo_sec.COLLNAME)
		coll_sec.delete_many({})

	def test_get_current_profile_success(self):
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)
		profile = adapter.register('test_name', 'test_password')

		self.assertIsInstance(profile, Profile)

		sec_repo = SecurityRepository(config())
		sec_adapter = LoginAdapter(repo, sec_repo, config())
		session = sec_adapter.login(profile.name, 'test_password')
		self.assertIsInstance(session, Session)

		current_profile_adapter = CurrentProfileAdapter(repo, sec_repo)
		name = current_profile_adapter.show()
		self.assertIsNotNone(name)
		self.assertEqual(name, profile.name)

	def test_get_current_profile_no_session(self):
		repo = ProfileRepository(config())
		sec_repo = SecurityRepository(config())

		current_profile_adapter = CurrentProfileAdapter(repo, sec_repo)
		name = current_profile_adapter.show()
		self.assertIsNone(name)
