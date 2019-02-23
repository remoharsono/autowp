import unittest
from bson.objectid import ObjectId

from autowp.apps.shared.base.exceptions import AuthError
from autowp.apps.shared.security.auth import auth

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
from autowp.apps.cli.adapter.security.logout import LogoutAdapter 

@auth
class FakeAdapterWithAuth(object):
	def __init__(self, msg='world'):
		self.msg = msg 

	def hello(self):
		return f'Hello {self.msg}'

class AuthDecoratorTestCase(unittest.TestCase):
	
	def tearDown(self):
		"""Will delete all documents after of each tests"""
		repo = ProfileRepository(config())
		coll = repo.build_mongo_coll(repo.COLLNAME)
		coll.delete_many({})
		
		repo_sec = SecurityRepository(config())
		coll_sec = repo_sec.build_mongo_coll(repo_sec.COLLNAME)
		coll_sec.delete_many({})

	def test_should_raise_auth_err(self):
		with self.assertRaises(AuthError):
			adapter = FakeAdapterWithAuth(msg='auth')

	def test_should_be_success_after_login(self):	
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)
		profile = adapter.register('test_name', 'test_password')
		self.assertIsInstance(profile, Profile)

		sec_repo = SecurityRepository(config())
		sec_adapter = LoginAdapter(repo, sec_repo, config())
		session = sec_adapter.login(profile.name, 'test_password')
		self.assertIsInstance(session, Session)

		adapter = FakeAdapterWithAuth(msg='auth')
		self.assertEqual('Hello auth', adapter.hello())

	def test_should_be_fail_after_logout(self):
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)
		profile = adapter.register('test_name', 'test_password')
		self.assertIsInstance(profile, Profile)

		sec_repo = SecurityRepository(config())
		sec_adapter = LoginAdapter(repo, sec_repo, config())
		session = sec_adapter.login(profile.name, 'test_password')
		self.assertIsInstance(session, Session)

		logout_adapter = LogoutAdapter(sec_repo, repo)
		logout_adapter.logout()

		with self.assertRaises(AuthError):
			adapter = FakeAdapterWithAuth(msg='auth')
			adapter.hello()
