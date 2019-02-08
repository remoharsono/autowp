from typing import NoReturn

from autowp.core.profile.usecase.base import BaseProfileUseCase

class DeleteUseCase(BaseProfileUseCase):

	def remove(self, name: str) -> bool:
		"""Delete profile from database
		
		Raises:
			core.shared.exceptions.VarTypeError: If given name is not a string
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		return self.repo.remove(name)
