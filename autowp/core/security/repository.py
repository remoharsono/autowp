from abc import abstractmethod
from typing import Optional, NoReturn

from autowp.core.security.entity import Session
from autowp.core.shared.base import Repository as BaseRepo

class SecurityRepo(BaseRepo):
	"""An interface of SecurityRepo
	
	This repo should be used to manage security sessions.
	"""

	@abstractmethod
	def register(self, session: Session) -> str:
		"""This method used to create new session
		
		This method must be return an id from database
		"""
		pass

	@abstractmethod
	def remove(self, id: str) -> bool:
		"""This method used to remove single session"""
		pass

	@abstractmethod
	def get(self, id: Optional[str] = None) -> Optional[Session]:
		"""This method used to get detail session

		Should be return None, if session not exist. We need to
		make id param as optional, it will give more flexibility
		to our caller.

		Our simple scenario is, just check from database for current
		session storage. If we have at least one, then just return 
		that session data.  If we doesn't have any session data in our
		session storage, then return None. If id has a valid value (not None),
		we need to get session based on id from database.

		Actually this method almost have same function with is_exist, but if 
		is_exist will return boolean value than an optional session data.
		"""
		pass

	@abstractmethod
	def is_exist(self, id: Optional[str] = None) -> bool:
		"""This method used to check if session exist or not"""
		pass

	@abstractmethod
	def lock(self, id: Optional[str] = None) -> NoReturn:
		"""This method used to set current session as locked"""
		pass

	@abstractmethod
	def unlock(self, id: Optional[str] = None) -> NoReturn:
		"""Used to unlock session"""
		pass
