from autowp.core.shared.base import UseCase 
from autowp.core.resource.repository import ResourceRepository  
from autowp.core.shared.utils import typechecker

class BaseResourceUseCase(UseCase):
	"""This is base class for all resource's usecases

	Attributes:
		repo: An instance of ResourceRepository
	"""

	def __init__(self, repo: ResourceRepository):
		"""Initialize repository
		
		Raises:
			core.shared.exceptions.VarTypeError: If repo is not an instance of ResourceRepository
		"""
		typechecker.check(repo, ResourceRepository, ('repo', 'ResourceRepository'))
		self.repo = repo
