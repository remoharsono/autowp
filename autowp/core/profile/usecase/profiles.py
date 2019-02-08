from typing import NoReturn, Optional, List

from autowp.core.profile.usecase.base import BaseProfileUseCase
from autowp.core.profile.entity import Profile
from autowp.core.profile.repository import Options

class ProfilesUseCase(BaseProfileUseCase):

	def profiles(self, options: Optional[Options]) -> Optional[List[Profile]]:
		"""Used to get a list of profiles (if any)
		
		Raises:
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""
		return self.repo.get_list(options)
