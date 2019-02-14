from autowp.core.profile.repository import ProfileRepository 
from autowp.core.profile.usecase.delete import DeleteUseCase

class DeleteAdapter(object):

	def __init__(self, repo: ProfileRepository):
		self.usecase = DeleteUseCase(repo)

	def remove(self, name: str) -> bool:
		"""Delete profile from database
		
		Raises:
			core.shared.exceptions.VarTypeError: If given name is not a string
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		check = self.usecase.repo.get_detail(name)
		if check:
			return self.usecase.remove(name)

		return False
