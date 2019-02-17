import unittest
from bson.objectid import ObjectId

from autowp.core.shared.exceptions import ValidationError
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

class LoginAdapterTestCase(unittest.TestCase):

	def tearDown(self):
		"""Will delete all documents after of each tests"""
		repo = ProfileRepository(config())
		coll = repo.build_mongo_coll(repo.COLLNAME)
		coll.delete_many({})

	def test_login_success(self):
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)
		profile = adapter.register('test_name', 'test_password')

		self.assertIsInstance(profile, Profile)
		self.assertIsInstance(profile.id, ObjectId)
		self.assertEqual('test_name', profile.name)
		self.assertIsNotNone(profile.password)
		self.assertIsNotNone(profile.id)

		sec_repo = SecurityRepository(config())
		sec_adapter = LoginAdapter(repo, sec_repo, config())
		session = sec_adapter.login(profile.name, 'test_password')
		self.assertIsInstance(session, Session)
		self.assertIsNotNone(session.profile_id)
		self.assertFalse(session.locked)
		self.assertIsNotNone(session.token)

	def test_login_failed_no_profile(self):
		repo = ProfileRepository(config())
		sec_repo = SecurityRepository(config())
		
		sec_adapter = LoginAdapter(repo, sec_repo, config())
		state = sec_adapter.login('unknown name', 'test_password')
		self.assertIsInstance(state, State)
		self.assertEqual(sec_adapter.usecase.STATE_NAME, state.name)
		self.assertEqual(sec_adapter.usecase.STATE_FAILED_NO_PROFILE, state.status)

	def test_login_failed_mismatch_password(self):
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)
		profile = adapter.register('test_name', 'test_password')
		
		sec_repo = SecurityRepository(config())		
		sec_adapter = LoginAdapter(repo, sec_repo, config())
		state = sec_adapter.login(profile.name, 'test_password_invalid')
		self.assertIsInstance(state, State)
		self.assertEqual(sec_adapter.usecase.STATE_NAME, state.name)
		self.assertEqual(sec_adapter.usecase.STATE_FAILED_PASSWORD_MISMTACH, state.status)

	def test_login_fail_validation(self):
		repo = ProfileRepository(config())
		sec_repo = SecurityRepository(config())		
		sec_adapter = LoginAdapter(repo, sec_repo, config())

		with self.assertRaises(ValidationError):
			state = sec_adapter.login(None, 'test_password_invalid')
