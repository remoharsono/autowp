from typing import NoReturn

from autowp.core.shared.utils import typechecker
from autowp.core.shared.base import UseCase 
from autowp.core.profile.repository import ProfileRepository

class DeleteUseCase(UseCase):
	"""A usecase used when removing profile from database

	Attributes:
		repo: Should be an instance of ProfileRepository
	"""
	def __init__(self, repo: ProfileRepository) -> NoReturn:
		"""Initialize object instance
		
		Raises:
			core.shared.exceptions.VarTypeError: If repo is not an instance of ProfileRepository
		"""
		typechecker.check(repo, ProfileRepository, ('repo', 'ProfileRepository'))
		self.repo = repo

	def remove(self, name: str) -> bool:
		"""Delete profile from database
		
		Raises:
			core.shared.exceptions.VarTypeError: If given name is not a string
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		return self.repo.remove(name)
