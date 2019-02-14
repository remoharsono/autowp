from typing import Optional, List

from autowp.core.profile.entity import Profile
from autowp.core.profile.repository import ProfileRepository 
from autowp.core.profile.usecase.profiles import ProfilesUseCase

class ProfilesAdapter(object):

	def __init__(self, repo: ProfileRepository):
		self.usecase = ProfilesUseCase(repo)

	def all(self, conditions: dict = {}, limit: int = 0, skip: int = 0) -> Optional[List[Profile]]:
		return self.usecase.profiles({
			'filter': conditions,
			'limit': limit,
			'skip': skip
		})
