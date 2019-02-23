from abc import abstractmethod
from typing import Dict, Optional, Any, List, NoReturn

from autowp.core.resource.entity import Server
from autowp.core.shared.base import Repository as BaseRepo

class ResourceRepository(BaseRepo):
	"""An interface of ResourceRepository"""

	@abstractmethod
	def create(self, server: Server) -> Optional[Server]:
		"""Create new resource

		We should check given server should be an instance of Server
		entity.
		
		Raises:
			core.shared.exceptions.VarTypeError: If profile is not an instance of Profile entity
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		pass

	@abstractmethod
	def update(self, conditions: Dict[str, Any], doc: Dict[str, Any]) -> Optional[Server]:
		"""Update registered server
		
		Raises:
			core.shared.exceptions.VarTypeError: If profile is not an instance of Profile entity
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		pass

	@abstractmethod
	def get_list(self, options: Optional[Dict[str, Any]] = None) -> Optional[List[Server]]:
		"""Get a list of registered resources
		
		Raises:
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		pass

	@abstractmethod
	def findById(self, id: str) -> Optional[Server]:
		"""Get single server entity by given id
		
		Raises:
			core.shared.exceptions.VarTypeError: If given id is not a string
		"""
		pass

	@abstractmethod
	def findByField(self, field: str, value: Any) -> Optional[Server]:
		"""Get single server entity based on field criteria
		
		Raises:
			core.shared.exceptions.VarTypeError: If given field is not a string
		"""
		pass

	@abstractmethod
	def remove(self, id: str) -> NoReturn:
		"""Remove server from database
		
		Raises:
			core.shared.exceptions.VarTypeError: If id name is not a string
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		pass
