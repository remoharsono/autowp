from typing import Optional

from autowp.core.shared.entity import State
from autowp.core.profile.entity import Profile, Password
from autowp.core.profile.repository import ProfileRepository
from autowp.core.security.repository import SecurityRepo 
from autowp.core.security.usecase.current_profile import CurrentProfileUseCase

class CurrentProfileAdapter(object):

	def __init__(self, repo_profile: ProfileRepository, repo_sec: SecurityRepo):
		self.usecase = CurrentProfileUseCase(repo_sec, repo_profile)

	def show(self) -> Optional[str]:
		try:
			profile = self.usecase.current_profile()
		except Exception as exc:
			return None
		else:
			if isinstance(profile, Profile):
				return profile.name

			return None
