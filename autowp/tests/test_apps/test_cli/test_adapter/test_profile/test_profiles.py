import unittest
from bson.objectid import ObjectId

from autowp.core.shared.exceptions import ValidationError
from autowp.core.profile.entity import Profile, Password
from autowp.apps.shared.config import config
from autowp.apps.shared.security.hasher import Sha256Hasher
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.cli.adapter.profile.register import RegisterAdapter
from autowp.apps.cli.adapter.profile.profiles import ProfilesAdapter 

class ProfilesAdapterTestCase(unittest.TestCase):
	
	def tearDown(self):
		"""Will delete all documents after of each tests"""
		repo = ProfileRepository(config())
		coll = repo.build_mongo_coll(repo.COLLNAME)
		coll.delete_many({})

	def test_get_all(self):
		repo = ProfileRepository(config())
		reg_adapter = RegisterAdapter(repo)

		profile1 = reg_adapter.register('test_name', 'test_password')
		profile2 = reg_adapter.register('test_name2', 'test_password')

		self.assertIsInstance(profile1, Profile)
		self.assertIsInstance(profile2, Profile)

		adapter = ProfilesAdapter(repo)
		profiles = adapter.all()

		self.assertIsNotNone(profiles)
		self.assertEqual(2, len(profiles))

		profile_2 = profiles[1]
		self.assertEqual(profile2.name, profile_2.name)

	def test_get_all_empty(self):
		repo = ProfileRepository(config())
		adapter = ProfilesAdapter(repo)
		profiles = adapter.all()
		self.assertIsNone(profiles)
