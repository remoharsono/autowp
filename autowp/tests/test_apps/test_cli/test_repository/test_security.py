import unittest
from bson.objectid import ObjectId

from autowp.core.shared.exceptions import StorageError, VarTypeError
from autowp.core.profile.entity import Profile, Password
from autowp.core.security.entity import Session, Token
from autowp.apps.shared.config import config
from autowp.apps.shared.security.hasher import Sha256Hasher
from autowp.apps.shared.security.tokenizer import JWTToken
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.cli.repository.security import SecurityRepository

class SecurityRepoTestCase(unittest.TestCase):

	def tearDown(self):
		"""Will delete all documents after of each tests"""
		repo = ProfileRepository(config())
		coll = repo.build_mongo_coll(repo.COLLNAME)
		coll.delete_many({})

		repo_sec = SecurityRepository(config())
		coll_sec = repo_sec.build_mongo_coll(repo_sec.COLLNAME)
		coll_sec.delete_many({})

	def test_register_session_success(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)

		repo = ProfileRepository(config())
		saved = repo.create(profile)
		self.assertTrue(saved)

		payload = {'name': profile.name}
		token = Token(salt='test_salt', payload=payload, builder=JWTToken)
		session = Session(token=token, locked=False, profile_id=saved.id)

		repo_sec = SecurityRepository(config())
		session_id = repo_sec.register(session)
		self.assertIsInstance(session_id, str)
		self.assertTrue(session_id != '')

	def test_register_session_invalid_session_var(self):
		repo_sec = SecurityRepository(config())
		with self.assertRaises(VarTypeError):
			session_id = repo_sec.register('test invalid')

	def test_is_exist_without_id_found(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)

		repo = ProfileRepository(config())
		saved = repo.create(profile)
		self.assertTrue(saved)

		payload = {'name': profile.name}
		token = Token(salt='test_salt', payload=payload, builder=JWTToken)
		session = Session(token=token, locked=False, profile_id=saved.id)

		repo_sec = SecurityRepository(config())
		session_id = repo_sec.register(session)
		self.assertIsInstance(session_id, str)
		self.assertTrue(session_id != '')
		self.assertTrue(repo_sec.is_exist())

	def test_is_exist_with_id_found(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)

		repo = ProfileRepository(config())
		saved = repo.create(profile)
		self.assertTrue(saved)

		payload = {'name': profile.name}
		token = Token(salt='test_salt', payload=payload, builder=JWTToken)
		session = Session(token=token, locked=False, profile_id=saved.id)

		repo_sec = SecurityRepository(config())
		session_id = repo_sec.register(session)
		self.assertIsInstance(session_id, str)
		self.assertTrue(session_id != '')
		self.assertTrue(repo_sec.is_exist(id=session_id))

	def test_is_exist_false_with_invalid_id(self):
		repo_sec = SecurityRepository(config())
		self.assertFalse(repo_sec.is_exist(id=str(ObjectId())))

	def test_is_exist_invalid_id(self):
		repo_sec = SecurityRepository(config())
		with self.assertRaises(StorageError):
			repo_sec.is_exist(id='invalid_id')

	def test_remove_success(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)

		repo = ProfileRepository(config())
		saved = repo.create(profile)
		self.assertTrue(saved)

		payload = {'name': profile.name}
		token = Token(salt='test_salt', payload=payload, builder=JWTToken)
		session = Session(token=token, locked=False, profile_id=saved.id)

		repo_sec = SecurityRepository(config())
		session_id = repo_sec.register(session)
		self.assertIsInstance(session_id, str)
		self.assertTrue(repo_sec.remove(session_id))
		self.assertFalse(repo_sec.is_exist())

	def test_get_session_success(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)

		repo = ProfileRepository(config())
		saved = repo.create(profile)
		self.assertTrue(saved)

		payload = {'name': profile.name}
		token = Token(salt='test_salt', payload=payload, builder=JWTToken)
		session = Session(token=token, locked=False, profile_id=saved.id)

		repo_sec = SecurityRepository(config())
		session_id = repo_sec.register(session)
		session = repo_sec.get(session_id)

		self.assertIsInstance(session, Session)
		self.assertEqual(session.token, token.build())
		self.assertEqual(session.profile_id, saved.id)
		self.assertFalse(session.locked)

	def test_get_session_none(self):
		repo_sec = SecurityRepository(config())
		session = repo_sec.get(str(ObjectId()))
		self.assertIsNone(session)

	def test_lock_success(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)

		repo = ProfileRepository(config())
		saved = repo.create(profile)
		self.assertTrue(saved)

		payload = {'name': profile.name}
		token = Token(salt='test_salt', payload=payload, builder=JWTToken)
		session = Session(token=token, locked=False, profile_id=saved.id)

		repo_sec = SecurityRepository(config())
		session_id = repo_sec.register(session)
		session = repo_sec.get(session_id)

		self.assertIsInstance(session, Session)
		self.assertEqual(session.token, token.build())
		self.assertEqual(session.profile_id, saved.id)
		self.assertFalse(session.locked)

		repo_sec.lock(id=session_id)
		session = repo_sec.get(session_id)
		self.assertTrue(session.locked)

	def test_unlock_success(self):
		password = Password(raw='test_password', hasher=Sha256Hasher)
		profile = Profile(name='test_name', password=password)

		repo = ProfileRepository(config())
		saved = repo.create(profile)
		self.assertTrue(saved)

		payload = {'name': profile.name}
		token = Token(salt='test_salt', payload=payload, builder=JWTToken)
		session = Session(token=token, locked=False, profile_id=saved.id)

		repo_sec = SecurityRepository(config())
		session_id = repo_sec.register(session)
		session = repo_sec.get(session_id)

		self.assertIsInstance(session, Session)
		self.assertEqual(session.token, token.build())
		self.assertEqual(session.profile_id, saved.id)
		self.assertFalse(session.locked)

		repo_sec.lock(id=session_id)
		session = repo_sec.get(session_id)
		self.assertTrue(session.locked)
		
		repo_sec.unlock(id=session_id)
		session = repo_sec.get(session_id)
		self.assertFalse(session.locked)
