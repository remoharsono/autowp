import unittest

from typing import Optional, Dict, Any, NoReturn, List

from autowp.core.shared.exceptions import ValidationError, VarTypeError

from autowp.core.profile.entity import Profile, Password
from autowp.core.profile.repository import ProfileRepository, Options

from autowp.core.security.entity import Session, Token
from autowp.core.security.repository import SecurityRepo
from autowp.core.security.usecase.login import LoginUseCase, LoginSuccessCallback

MEMORY = {}

class MemorySecurityRepo(SecurityRepo):
	
	def __init__(self, memory):
		self.in_memory = memory 

	def register(self, session: Session) -> str:
		id = str(uuid.uuid4()) 
		sess = Session(id, session.token, False) 
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

class BaseUseCaseSecurity(unittest.TestCase):

	def test_invalid_security_repo(self):
		repo_profile = MemoryProfileRepo(MEMORY)

		with self.assertRaises(VarTypeError):
			login_uc = LoginUseCase('test str', repo_profile)		

	def test_invalid_profile_repo(self):
		repo = MemorySecurityRepo(MEMORY)

		with self.assertRaises(VarTypeError):
			login_uc = LoginUseCase(repo, 'test str')		
