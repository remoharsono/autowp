import unittest
from typing import Optional, List

from autowp.core.profile.entity import Profile
from autowp.core.profile.repository import ProfileRepository, Options
from autowp.core.profile.usecase.register import RegisterUseCase
from autowp.core.shared.exceptions import ValidationError

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
		pass

class TestRegisterTestCase(unittest.TestCase):

	def test_register_success(self):
		repo = MemoryProfileRepo()
		usecase = RegisterUseCase(repo)
		profile = Profile('myname', 'mypassword')

		self.assertTrue(usecase.register(profile))

	def test_register_validation_no_name(self):
		with self.assertRaises(ValidationError):
			repo = MemoryProfileRepo()
			usecase = RegisterUseCase(repo)
			profile = Profile('', 'mypassword')
			usecase.register(profile)

	def test_register_validation_name_exist(self):
		with self.assertRaises(ValidationError):
			repo = MemoryProfileRepo()
			usecase = RegisterUseCase(repo)
			profile = Profile('name', 'mypassword')
			
			usecase.register(profile) # should be success
			usecase.register(profile) # name should be cannot pass validation

	def test_register_validation_no_password(self):
		with self.assertRaises(ValidationError):
			repo = MemoryProfileRepo()
			usecase = RegisterUseCase(repo)
			profile = Profile('name', '')
			usecase.register(profile)
