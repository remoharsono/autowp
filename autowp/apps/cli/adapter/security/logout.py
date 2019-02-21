from autowp.core.security.usecase.logout import LogoutUseCase
from autowp.apps.cli.repository.profile import ProfileRepository
from autowp.apps.cli.repository.security import SecurityRepository

class LogoutAdapter(object):

	def __init__(self, repo: SecurityRepository, repo_profile: ProfileRepository):
		self.usecase = LogoutUseCase(repo, repo_profile)

	def logout(self):
		"""Logout current logged in user

		Removing existing token from database

		Raises:
			autowp.core.shared.exceptions.StorageError
		"""
		self.usecase.logout()
