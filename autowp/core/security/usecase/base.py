from autowp.core.shared.base import UseCase 
from autowp.core.shared.utils import typechecker

from autowp.core.profile.repository import ProfileRepository
from autowp.core.security.repository import SecurityRepo

class BaseSecurityUseCase(UseCase):
	"""This is a base class for all security's usecases

	Attributes:
		repo: Should be an instance of SecurityRepository
		repo_profile: Should be an instance of ProfileRepository
	"""

	def __init__(self, repo: SecurityRepo, repo_profile: ProfileRepository):
		"""Initialize object instance
		
		Raises:
			core.shared.exceptions.VarTypeError: If repo is not an instance of SecurityRepository or ProfileRepository
		"""
		typechecker.check(repo, SecurityRepo, ('repo', 'SecurityRepo'))
		typechecker.check(repo_profile, ProfileRepository, ('repo_profile', 'ProfileRepository'))

		self.repo = repo
		self.repo_profile = repo_profile
