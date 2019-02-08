from typing import Optional

from autowp.core.shared.utils import typechecker
from autowp.core.shared.entity import State

from autowp.core.security.usecase.base import BaseSecurityUseCase
from autowp.core.security.entity import Session

from autowp.core.profile.entity import Profile

class CurrentProfileUseCase(BaseSecurityUseCase):
	"""A usecase to show current logging in profile

	To show current logged in, we need to know current session.
	If no session exist, then return None.
	If session exist, we need to extract session payload and create
	profile entity.
	"""

	def current_profile(self) -> Optional[Profile]:
		"""Current profile used to get current logged in profile
		
		Raises:
			autowp.core.shared.exceptions.VarTypeError
		"""
		if not self.repo.is_exist():
			return None

		session = self.repo.get()
		typechecker.check(session, Session, ('session', 'Session'))

		profile = self.repo_profile.id(session.profile_id)
		typechecker.check(profile, Profile, ('profile', 'Profile'))

		return profile
