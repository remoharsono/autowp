from typing import Optional

from autowp.core.resource.entity import Server
from autowp.core.resource.usecase.base import BaseResourceUseCase
from autowp.core.shared.utils import typechecker
from autowp.core.resource.utils.validation import ValidateResource

class CreateNewResourceUseCase(BaseResourceUseCase, ValidateResource):

	def register(self, server: Server) -> Optional[Server]:
		"""Register new resource server

		Validation rules:
		- We need to check if server's profile_id is not empty
		- We need to check if given server's host is not empty 
		- We need to check if given server's host has been registered or not
		- We need to check if given server's user name is not empty
		
		Raises:
			core.shared.exceptions.VarTypeError: If profile is not an instance of Profile entity
			core.shared.exceptions.ValidationError: if profile not passed validation process
			core.shared.exceptions.StorageError: if there is an error related with datastorage 
		"""
		typechecker.check(server, Server, ('server', 'Server'))

		# validate input
		self.validate(server, repo=self.repo)

		return self.repo.create(server)
