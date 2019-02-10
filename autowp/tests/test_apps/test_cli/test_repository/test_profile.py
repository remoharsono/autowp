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
		saved = repo.create(profile)
		self.assertTrue(saved)
		self.assertEqual(saved.name, profile.name)
		self.assertEqual(saved.password, profile.password.to_hash())
		self.assertIsNotNone(saved.id)

	def test_get_by_name(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)
		
		repo = ProfileRepository(config())
		self.assertTrue(repo.create(profile))

		doc = repo.get_detail(profile.name)
		self.assertIsNotNone(doc)
		self.assertEqual(doc.name, profile.name)
	
	def test_get_by_id(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)
		
		repo = ProfileRepository(config())
		self.assertTrue(repo.create(profile))

		doc_by_name = repo.get_detail(profile.name)

		self.assertIsNotNone(doc_by_name)
		self.assertEqual(doc_by_name.name, profile.name)

		doc_by_id = repo.id(doc_by_name.id)
		self.assertIsNotNone(doc_by_id)

	def test_remove_success(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)
		
		repo = ProfileRepository(config())
		self.assertTrue(repo.create(profile))
		self.assertTrue(repo.remove(profile.name))

		doc = repo.get_detail(profile.name)
		self.assertIsNone(doc)

	def test_get_list(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)
		
		password2 = Password(raw='test_password', hasher=Sha256Hasher)
		profile2 = Profile(name='test_name', password=password)
		
		repo = ProfileRepository(config())
		repo.create(profile)
		repo.create(profile2)

		docs = repo.get_list({
			'filter': {'name': 'test_name'}
		})

		self.assertIsInstance(docs, list)
		self.assertEqual(2, len(docs))

		doc1 = docs[0]
		self.assertEqual(doc1.name, profile.name)

	def test_get_list_empty(self):
		repo = ProfileRepository(config())
		docs = repo.get_list({
			'filter': {'name': 'test_name'}
		})

		self.assertIsNone(docs)

	def test_get_list_not_dict(self):
		repo = ProfileRepository(config())
		docs = repo.get_list('invalid')
		self.assertIsNone(docs)

	def test_get_list_no_options(self):
		repo = ProfileRepository(config())
		docs = repo.get_list()
		self.assertIsNone(docs)

	def test_create_invalid_profile(self):
		with self.assertRaises(VarTypeError):
			repo = ProfileRepository(config())
			repo.create('testing')
