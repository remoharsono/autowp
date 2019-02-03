from typing import NoReturn

from autowp.core.shared.base import UseCase 
from autowp.core.profile.repository import ProfileRepository
from autowp.core.shared.utils import typechecker

class BaseProfileUseCase(UseCase):
	"""This is a base class for all profile's usecases

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
