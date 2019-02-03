import unittest
import hashlib
from typing import Optional, List

from autowp.core.shared.utils import typechecker
from autowp.core.shared.exceptions import VarTypeError
from autowp.core.shared.base import PasswordHasher

from autowp.core.profile.entity import Profile, Password
from autowp.core.profile.repository import ProfileRepository, Options
from autowp.core.profile.usecase.register import RegisterUseCase
from autowp.core.profile.usecase.delete import DeleteUseCase 

class Sha256Hasher(PasswordHasher):

	def hash(self) -> str:
		hasher = hashlib.new('sha256')
		if self.raw != '':
			hasher.update(self.raw.encode())
			return hasher.hexdigest()

		return self.raw

class MemoryProfileRepo(ProfileRepository):

	def __init__(self):
		self.in_memory = {}

	def create(self, profile: Profile) -> bool:
		self.in_memory[profile.name] = profile
		return True

	def get_list(self, options: Options) -> List[Profile]:
		pass 

	def get_detail(self, name: str) -> Optional[Profile]:
		if name in self.in_memory:
			return self.in_memory.get(name)

		return None

	def remove(self, name: str) -> bool:
		typechecker.check(name, str, ('name', 'str'))

		check = self.get_detail(name)
		if check:
			del self.in_memory[name]
			return True

		return False 

class DeleteProfileTestCase(unittest.TestCase):

	def test_delete_success(self):
		repo = MemoryProfileRepo()
		profile = Profile('myname', Password('mypassword', Sha256Hasher))
		
		register_case = RegisterUseCase(repo)
		delete_case = DeleteUseCase(repo)

		self.assertTrue(register_case.register(profile))
		self.assertTrue(delete_case.remove(profile.name))

		check = repo.get_detail(profile.name)
		self.assertIsNone(check)

	def test_delete_mismatch_type(self):
		with self.assertRaises(VarTypeError):
			repo = MemoryProfileRepo()
			delete_case = DeleteUseCase(repo)
			delete_case.remove(12)

	def test_delete_not_exist(self):
		repo = MemoryProfileRepo()
		delete_case = DeleteUseCase(repo)

		self.assertFalse(delete_case.remove('not existing name'))
