import unittest
from bson.objectid import ObjectId

from autowp.core.shared.exceptions import ValidationError
from autowp.core.profile.entity import Profile, Password
from autowp.apps.shared.config import config
from autowp.apps.shared.security.hasher import Sha256Hasher
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.cli.adapter.profile.register import RegisterAdapter
from autowp.apps.cli.adapter.profile.delete import DeleteAdapter 

class DeleteAdapterTestCase(unittest.TestCase):

	def tearDown(self):
		"""Will delete all documents after of each tests"""
		repo = ProfileRepository(config())
		coll = repo.build_mongo_coll(repo.COLLNAME)
		coll.delete_many({})

	def test_delete_success(self):
		repo = ProfileRepository(config())
		reg_adapter = RegisterAdapter(repo)
		del_adapter = DeleteAdapter(repo)

		profile = reg_adapter.register('test_name', 'test_password')

		self.assertIsInstance(profile, Profile)
		self.assertIsInstance(profile.id, ObjectId)
		self.assertEqual('test_name', profile.name)
		self.assertIsNotNone(profile.password)
		self.assertIsNotNone(profile.id)
		self.assertTrue(del_adapter.remove(profile.name))
		self.assertIsNone(repo.get_detail(profile.name))

	def test_delete_failed(self):
		repo = ProfileRepository(config())
		del_adapter = DeleteAdapter(repo)
		self.assertFalse(del_adapter.remove('not exist name'))
