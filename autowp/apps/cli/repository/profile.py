from typing import Optional, List
from pymongo.errors import PyMongoError

from autowp.core.shared.utils import typechecker
from autowp.core.shared.exceptions import VarTypeError, StorageError
from autowp.core.profile.entity import Profile
from autowp.core.profile.repository import ProfileRepository as ProfileRepoInterface, Options
from autowp.apps.shared.base.repository import BaseRepository

class ProfileRepository(ProfileRepoInterface, BaseRepository):

	COLLNAME = 'profiles'

	def create(self, profile: Profile) -> bool:
		"""Create new user profile
		
		Raises:
			core.shared.exceptions.VarTypeError: If profile is not an instance of Profile entity
			core.shared.exceptions.StorageError: If there is an error relate with storage
		"""

		# need to check profile, make sure if it's an instance of Profile
		typechecker.check(profile, Profile, ('profile', 'Profile'))
		try:
			# build coll object instance
			coll = self.build_mongo_coll(self.COLLNAME)

			# initialize doc payload
			payload = {'name': profile.name}

			if profile.password.hashed:
				payload['password'] = profile.password.hashed
			else:
				payload['password'] = profile.password.to_hash()

			created = coll.insert_one(payload)
			if created:
				return True

			return False
		except PyMongoError as exc_pymongo:
			raise StorageError(exc_pymongo)

	def get_list(self, options: Optional[Options] = None) -> Optional[List[Profile]]:
		pass

	def get_detail(self, name: str) -> Optional[Profile]:
		pass

	def id(self, id: str) -> Optional[Profile]:
		pass

	def remove(self, name: str) -> bool:
		pass
