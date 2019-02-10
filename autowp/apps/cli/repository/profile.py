from typing import Optional, List
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from autowp.core.shared.utils import typechecker
from autowp.core.shared.exceptions import VarTypeError, StorageError
from autowp.core.profile.entity import Profile
from autowp.core.profile.repository import ProfileRepository as ProfileRepoInterface, Options
from autowp.apps.shared.base.repository import BaseRepository
from autowp.apps.shared.security.hasher import Sha256Hasher

class ProfileRepository(ProfileRepoInterface, BaseRepository):

	COLLNAME = 'profiles'

	def create(self, profile: Profile) -> Profile:
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
			saved_profile = Profile(
				id=created.inserted_id, 
				name=profile.name, 
				password=payload.get('password')
			)

			return saved_profile
		except PyMongoError as exc_pymongo:
			raise StorageError(exc_pymongo)

	def get_list(self, options: Optional[Options] = None) -> Optional[List[Profile]]:
		if not options:
			return None

		if not isinstance(options, dict):
			return None

		coll = self.build_mongo_coll(self.COLLNAME)
		payload = options.get('filter', {})
		skip = options.get('skip', 0)
		limit = options.get('limit', 0)

		docs = coll.find(filter=payload, skip=skip, limit=limit)
		if docs.count() >= 1:
			profiles = []
			for doc in docs:
				profile = Profile(
					id=doc.get('_id'), 
					name=doc.get('name'), 
					password=doc.get('password')
				)

				profiles.append(profile)

			return profiles

		return None

	def get_detail(self, name: str) -> Optional[Profile]:
		coll = self.build_mongo_coll(self.COLLNAME)
		doc = coll.find_one({'name': name})
		if not doc:
			return None
		
		profile = Profile(id=doc.get('_id'), name=doc.get('name'), password=doc.get('password'))
		return profile

	def id(self, id: str) -> Optional[Profile]:
		coll = self.build_mongo_coll(self.COLLNAME)
		doc = coll.find_one({'_id': ObjectId(id)})
		if not doc:
			return None
		
		profile = Profile(id=doc.get('_id'), name=doc.get('name'), password=doc.get('password'))
		return profile

	def remove(self, name: str) -> bool:
		coll = self.build_mongo_coll(self.COLLNAME)
		coll.delete_one({'name': name})
		return True
