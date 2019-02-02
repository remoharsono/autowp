from typing import NoReturn, Optional, List

from autowp.core.shared.utils import typechecker
from autowp.core.shared.base import UseCase 
from autowp.core.profile.entity import Profile
from autowp.core.profile.repository import ProfileRepository, Options

class ProfilesUseCase(UseCase):
	"""A usecase used when get a list of registered profiles
	
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

	def profiles(self, options: Optional[Options]) -> Optional[List[Profile]]:
		"""Used to get a list of profiles (if any)
		
		Raises:
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		return self.repo.get_list(options)
