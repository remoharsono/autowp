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
	def get(self, id: str) -> Optional[Session]:
		"""This method used to get detail session

		Should be return None, if session not exist
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
