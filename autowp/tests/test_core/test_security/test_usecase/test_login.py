import unittest
import json
import base64
import hashlib
import uuid

from typing import Optional, Dict, Any, NoReturn, List

from autowp.core.profile.entity import Profile, Password
from autowp.core.profile.repository import ProfileRepository, Options

from autowp.core.security.entity import Session, Token
from autowp.core.security.repository import SecurityRepo
from autowp.core.security.usecase.login import LoginUseCase, LoginSuccessCallback

from autowp.core.shared.exceptions import ValidationError, VarTypeError
from autowp.core.shared.base import PasswordHasher, Tokenizer
from autowp.core.shared.entity import State

SALT = '123'
MEMORY = {}
MEMORY_SESSION = {}

def _on_success_cb(salt: str, profile: Profile) -> Session:
	payload = {'name': profile.name}
	token = Token(salt, payload, HashlibToken)
	sess = Session(token, False) 
	return sess

class HashlibToken(Tokenizer):

	def encode(self) -> str:
		payload = json.dumps(self.payload)
		b64 = base64.b64encode(payload.encode())
		return b64.decode()

	def decode(self, token: str) -> Optional[Dict[str, Any]]:
		pass

class Sha256Hasher(PasswordHasher):

	def hash(self) -> str:
		hasher = hashlib.new('sha256')
		if self.raw != '':
			hasher.update(self.raw.encode())
			return hasher.hexdigest()

		return self.raw

class MemorySecurityRepo(SecurityRepo):
	
	def __init__(self, memory):
		self.in_memory = memory 

	def register(self, session: Session) -> str:
		id = str(uuid.uuid4())
		sess = Session(token=session.token, locked=False, profile_id=session.profile_id, id=id) 
		self.in_memory[id] = sess
		return id
	
	def remove(self, id: str) -> bool:
		"""This method used to remove single session"""
		pass

	def get(self, id: str) -> Optional[Session]:
		"""This method used to get detail session

		Should be return None, if session not exist
		"""
		pass

	def is_exist(self, id: Optional[str] = None) -> bool:
		"""This method used to check if session exist or not"""
		pass

	def lock(self, id: Optional[str] = None) -> NoReturn:
		"""This method used to set current session as locked"""
		pass
	
	def unlock(self, id: Optional[str] = None) -> NoReturn:
		"""This method used to set current session as locked"""
		pass

class MemoryProfileRepo(ProfileRepository):
	def __init__(self, memory):
		self.in_memory = memory 

	def create(self, profile: Profile) -> Profile:
		new_password = Password(profile.password.raw, Sha256Hasher, profile.password.to_hash())
		new_profile = Profile(profile.name, new_password)
		self.in_memory[profile.name] = new_profile
		return new_profile 

	def get_list(self, options: Options) -> List[Profile]:
		pass 

	def get_detail(self, name: str) -> Optional[Profile]:
		if name in self.in_memory:
			return self.in_memory.get(name)

		return None
	
	def id(self, id: str) -> Optional[Profile]:
		pass

	def remove(self, name: str) -> bool:
		typechecker.check(name, str, ('name', 'str'))

		check = self.get_detail(name)
		if check:
			del self.in_memory[name]
			return True

		return False 


class LoginUseCaseTestCase(unittest.TestCase):

	def test_success(self):
		repo = MemorySecurityRepo(MEMORY_SESSION)
		repo_profile = MemoryProfileRepo(MEMORY)

		profile = Profile('test', Password('test', Sha256Hasher))
		self.assertTrue(repo_profile.create(profile))

		login_uc = LoginUseCase(repo, repo_profile)
		session = login_uc.login(SALT, profile, _on_success_cb)
		
		self.assertFalse(isinstance(session, State))
		self.assertIsNotNone(session.id)
		self.assertIsNone(session.token.options)
		self.assertTrue(isinstance(session.token.build(), str))

	def test_profile_not_exist(self):
		repo = MemorySecurityRepo(MEMORY_SESSION)
		repo_profile = MemoryProfileRepo(MEMORY)

		profile = Profile('test', Password('test', Sha256Hasher))
		login_uc = LoginUseCase(repo, repo_profile)

		session = login_uc.login(SALT, profile, _on_success_cb)

		self.assertIsInstance(session, State)
		self.assertEqual(session.name, login_uc.STATE_NAME)
		self.assertEqual(session.status, login_uc.STATE_FAILED_NO_PROFILE)

	def test_profile_password_mismatch(self):
		repo = MemorySecurityRepo(MEMORY_SESSION)
		repo_profile = MemoryProfileRepo(MEMORY)

		profile = Profile('test', Password('test', Sha256Hasher))
		self.assertTrue(repo_profile.create(profile))

		profile_invalid = Profile('test', Password('test2', Sha256Hasher))
		login_uc = LoginUseCase(repo, repo_profile)
		session = login_uc.login(SALT, profile_invalid, _on_success_cb)

		self.assertIsInstance(session, State)
		self.assertEqual(session.name, login_uc.STATE_NAME)
		self.assertEqual(session.status, login_uc.STATE_FAILED_PASSWORD_MISMTACH)

	def test_profile_not_valid_no_name(self):
		repo = MemorySecurityRepo(MEMORY_SESSION)
		repo_profile = MemoryProfileRepo(MEMORY)

		profile = Profile('', Password('test', Sha256Hasher))
		login_uc = LoginUseCase(repo, repo_profile)
		
		with self.assertRaises(ValidationError):
			session = login_uc.login(SALT, profile, _on_success_cb)

	def test_profile_not_valid_no_password(self):
		repo = MemorySecurityRepo(MEMORY_SESSION)
		repo_profile = MemoryProfileRepo(MEMORY)

		profile = Profile('test', Password('', Sha256Hasher))
		login_uc = LoginUseCase(repo, repo_profile)
		
		with self.assertRaises(ValidationError):
			session = login_uc.login(SALT, profile, _on_success_cb)

	def test_invalid_profile_type(self):
		repo = MemorySecurityRepo(MEMORY_SESSION)
		repo_profile = MemoryProfileRepo(MEMORY)

		login_uc = LoginUseCase(repo, repo_profile)		
		with self.assertRaises(VarTypeError):
			session = login_uc.login(SALT, 'test str', _on_success_cb)
