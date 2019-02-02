from abc import abstractmethod
from typing import List, Optional, Any, Dict

from autowp.core.profile.entity import Profile
from autowp.core.shared.base import Repository as BaseRepo

Options = Dict[str, Any]

class ProfileRepository(BaseRepo):
	"""An interface of ProfileRepository"""

	@abstractmethod
	def create(self, profile: Profile) -> bool:
		"""Create new user profile

		We should check profile parameter is an instance of Profile or not
		before continue to main process.

		Raises:
			core.shared.exceptions.VarTypeError: If profile is not an instance of Profile entity
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		pass

	@abstractmethod
	def get_list(self, options: Options) -> Optional[List[Profile]]:
		"""Get a list of registered profiles

		Raises:
			core.shared.exceptions.StorageError: If there is an error relate with storage
		Returns:
			A list of profile or a None value if there is no profiles yet
		"""
		pass

	@abstractmethod
	def get_detail(self, name: str) -> Optional[Profile]:
		"""Get a detail profile by given name

		Raises:
			core.shared.exceptions.VarTypeError: If given name is not a string
		"""
		pass

	@abstractmethod
	def remove(self, name: str) -> bool:
		"""Remove profile from database
		
		Raises:
			core.shared.exceptions.VarTypeError: If given name is not a string
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		pass
