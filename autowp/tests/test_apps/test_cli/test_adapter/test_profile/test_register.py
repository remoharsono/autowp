import unittest
from bson.objectid import ObjectId

from autowp.core.shared.exceptions import ValidationError
from autowp.core.profile.entity import Profile, Password
from autowp.apps.shared.config import config
from autowp.apps.shared.security.hasher import Sha256Hasher
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.cli.adapter.profile.register import RegisterAdapter

class RegisterAdapterTestCase(unittest.TestCase):
	
	def tearDown(self):
		"""Will delete all documents after of each tests"""
		repo = ProfileRepository(config())
		coll = repo.build_mongo_coll(repo.COLLNAME)
		coll.delete_many({})

	def test_register_success(self):
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)
		profile = adapter.register('test_name', 'test_password')

		self.assertIsInstance(profile, Profile)
		self.assertIsInstance(profile.id, ObjectId)
		self.assertEqual('test_name', profile.name)
		self.assertIsNotNone(profile.password)
		self.assertIsNotNone(profile.id)

	def test_register_no_name(self):
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)

		with self.assertRaises(ValidationError):
			adapter.register(None, 'test_pass')

	def test_register_name_exist(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)
		
		repo = ProfileRepository(config())
		saved = repo.create(profile)
		
		adapter = RegisterAdapter(repo)
		with self.assertRaises(ValidationError):
			adapter.register(saved.name, 'test_pass')

	def test_register_no_pass(self):
		repo = ProfileRepository(config())
		adapter = RegisterAdapter(repo)

		with self.assertRaises(ValidationError):
			adapter.register('test_name', '')
