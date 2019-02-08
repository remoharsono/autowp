from typing import Optional, NoReturn

from autowp.core.shared.entity import State
from autowp.core.security.usecase.base import BaseSecurityUseCase
from autowp.core.security.entity import Session

class LogoutUseCase(BaseSecurityUseCase):
	"""This usecase used to destroying current user's session

	Our system should be able to remove current user's session.
	May use a given id (optional) or not.

	All of these processes should not give any side effects like
	throwing exceptions.
	"""

	def logout(self, id: Optional[str] = None) -> NoReturn:
		"""Logout used to destroy current user's session

		We doesnt need to return any values from this method.
		If id is not None, then we need to check a session based
		on given id, and delete it from database.

		If id is None, then we need to check for any available sessions
		from database and destroy it.

		Repo flows:
		- use is_exist
		- if session exist, then get the session data
		- use valid id and use remove 
		"""
		if self.repo.is_exist(id=id):
			session = self.repo.get(id=id)
			if session:
				# remove current session
				self.repo.remove(session.id)
