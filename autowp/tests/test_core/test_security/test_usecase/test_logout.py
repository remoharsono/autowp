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
from autowp.core.security.usecase.logout import LogoutUseCase
from autowp.core.security.usecase.login import LoginUseCase, LoginSuccessCallback

from autowp.core.shared.base import PasswordHasher, Tokenizer
from autowp.core.shared.entity import State

SALT = '123'
MEMORY = {}
MEMORY_SESSION = {}

def _on_success_cb(salt: str, profile: Profile) -> Session:
	payload = {'name': profile.name}
	token = Token(salt, payload, HashlibToken)
	sess = Session(token=token, locked=False) 
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
		sess = Session(id=id, token=session.token, locked=False) 
		self.in_memory[id] = sess
		return id
	
	def remove(self, id: str) -> bool:
		"""This method used to remove single session"""
		if id not in self.in_memory:
			return False

		del self.in_memory[id]
		return True

	def get(self, id: Optional[str] = None) -> Optional[Session]:
		"""This method used to get detail session

		Should be return None, if session not exist
		"""
		if id is not None:
			return self.in_memory.get(id)
		else:
			if self.in_memory:
				keys = list(self.in_memory.keys())
				return self.in_memory[keys[0]]

		return None

	def is_exist(self, id: Optional[str] = None) -> bool:
		"""This method used to check if session exist or not"""
		if id is not None:
			return id in self.in_memory
		else:
			return len(self.in_memory) >= 1

	def lock(self, id: Optional[str] = None) -> NoReturn:
		"""This method used to set current session as locked"""
		pass
	
	def unlock(self, id: Optional[str] = None) -> NoReturn:
		"""This method used to set current session as locked"""
		pass

class MemoryProfileRepo(ProfileRepository):
	def __init__(self, memory):
		self.in_memory = memory 

	def create(self, profile: Profile) -> bool:
		new_password = Password(profile.password.raw, Sha256Hasher, profile.password.to_hash())
		self.in_memory[profile.name] = Profile(profile.name, new_password) 
		return True

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

class LogoutUseCaseTestCase(unittest.TestCase):

	def test_session_deleted(self):
		repo = MemorySecurityRepo(MEMORY_SESSION)
		repo_profile = MemoryProfileRepo(MEMORY)

		profile = Profile('test', Password('test', Sha256Hasher))
		self.assertTrue(repo_profile.create(profile))

		login_uc = LoginUseCase(repo, repo_profile)
		session = login_uc.login(SALT, profile, _on_success_cb)

		self.assertFalse(isinstance(session, State))
		self.assertIsNotNone(session.id)

		logout_uc = LogoutUseCase(repo, repo_profile)
		logout_uc.logout(session.id)

		self.assertFalse(repo.is_exist(session.id))

	def test_delete_unknown_session(self):
		repo = MemorySecurityRepo(MEMORY_SESSION)
		repo_profile = MemoryProfileRepo(MEMORY)

		profile = Profile('test', Password('test', Sha256Hasher))
		self.assertTrue(repo_profile.create(profile))

		login_uc = LoginUseCase(repo, repo_profile)
		session = login_uc.login(SALT, profile, _on_success_cb)
		self.assertFalse(isinstance(session, State))
		self.assertIsNotNone(session.id)

		logout_uc = LogoutUseCase(repo, repo_profile)
		logout_uc.logout('unknown id')
		self.assertTrue(repo.is_exist())

	def test_delete_session_using_none(self):
		repo = MemorySecurityRepo(MEMORY_SESSION)
		repo_profile = MemoryProfileRepo(MEMORY)

		profile = Profile('test', Password('test', Sha256Hasher))
		self.assertTrue(repo_profile.create(profile))

		login_uc = LoginUseCase(repo, repo_profile)
		session = login_uc.login(SALT, profile, _on_success_cb)
		self.assertFalse(isinstance(session, State))
		self.assertIsNotNone(session.id)

		logout_uc = LogoutUseCase(repo, repo_profile)
		logout_uc.logout()
		self.assertFalse(repo.is_exist())
