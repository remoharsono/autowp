from typing import Optional, NoReturn
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from bson.errors import InvalidId

from autowp.core.shared.utils import typechecker
from autowp.core.shared.exceptions import VarTypeError, StorageError
from autowp.core.security.repository import SecurityRepo as SecurityRepoInterface
from autowp.core.security.entity import Session
from autowp.apps.shared.base.repository import BaseRepository

class SecurityRepository(SecurityRepoInterface, BaseRepository):
	COLLNAME = 'sessions'

	def register(self, session: Session) -> str:
		"""Used to save given session to database"""

		# need to check given session variable
		typechecker.check(session, Session, ('session', 'Session'))

		try:
			# build coll object instance
			coll = self.build_mongo_coll(self.COLLNAME)

			# build payload
			payload = {
				'profile_id': session.profile_id, 
				'token': session.token.build().decode(),
				'locked': session.locked
			}

			created = coll.insert_one(payload)
			if created:
				return str(created.inserted_id) 

			return ''
		except PyMongoError as exc_pymongo:
			raise StorageError(exc_pymongo)

	def remove(self, id: str) -> bool:
		"""Remove session from database"""
		coll = self.build_mongo_coll(self.COLLNAME)
		coll.delete_one({'_id': ObjectId(id)})
		return True

	def get(self, id: Optional[str] = None) -> Optional[Session]:
		"""Get detail session from database

		We can use id or not. If id not available, we just need to count
		at least one record, if exist then load it.
		"""
		try:
			# build coll object instance
			coll = self.build_mongo_coll(self.COLLNAME)
			condition = {}

			if id:
				condition['_id'] = ObjectId(id) 

			sess = coll.find_one(filter=condition)
			if not sess:
				return None

			session = Session(
				token=sess.get('token'), 
				locked=sess.get('locked'),
				profile_id=str(sess.get('profile_id')),
				id=str(sess.get('_id'))
			)

			return session
		except PyMongoError as exc_pymongo:
			raise StorageError(exc_pymongo)
		except InvalidId as exc_invalid_id:
			raise StorageError(exc_invalid_id)

	def is_exist(self, id: Optional[str] = None) -> bool:
		"""Used to check if there is at least one session available

		If id not available, then we just need to get at least one variable
		and load it
		"""
		try:
			# build coll object instance
			coll = self.build_mongo_coll(self.COLLNAME)
			condition = {}

			if id:
				condition['_id'] = ObjectId(id) 

			sess = coll.find_one(filter=condition)
			return True if sess else False
		except PyMongoError as exc_pymongo:
			raise StorageError(exc_pymongo)
		except InvalidId as exc_invalid_id:
			raise StorageError(exc_invalid_id)

	def lock(self, id: Optional[str] = None) -> NoReturn:
		"""Used to change locked status to True"""
		try:
			pass
			# build coll object instance
			coll = self.build_mongo_coll(self.COLLNAME)
			sess = self.get(id=id)
			if sess:
				coll.replace_one({'_id': ObjectId(id)}, {'locked': True})
		except PyMongoError as exc_pymongo:
			raise StorageError(exc_pymongo)
		except InvalidId as exc_invalid_id:
			raise StorageError(exc_invalid_id)

	def unlock(self, id: Optional[str] = None) -> NoReturn:
		"""Used to change locked status to False"""
		try:
			pass
			# build coll object instance
			coll = self.build_mongo_coll(self.COLLNAME)
			sess = self.get(id=id)
			if sess:
				coll.replace_one({'_id': ObjectId(id)}, {'locked': False})
		except PyMongoError as exc_pymongo:
			raise StorageError(exc_pymongo)
		except InvalidId as exc_invalid_id:
			raise StorageError(exc_invalid_id)
