from typing import Union, Callable

from autowp.core.shared.utils import typechecker
from autowp.core.shared.entity import State

from autowp.core.security.usecase.base import BaseSecurityUseCase
from autowp.core.security.entity import Session

from autowp.core.profile.utils.validation import ValidateProfile
from autowp.core.profile.entity import Profile

'''
Example success callback:

def _on_success_callback(salt: str, profile: Profile) -> Session:
	pass

You need to create a Session object inside your callback
'''
LoginSuccessCallback = Callable[[str, Profile], Session]

class LoginUseCase(BaseSecurityUseCase, ValidateProfile):
	"""This usecase used to manage login activity

	Login activity will need two repositories:
	- ProfileRepository
	- SecurityRepository

	ProfileRepository will used to fetch user's profile data
	based on given profile request.

	This class also need to compare between profile fetched from 
	database and given profile from request, and compare the hashed
	password. If match, then we should create a session token
	and save it in database using SecurityRepository.
	"""

	STATE_NAME = 'user_logging_in'
	STATE_FAILED_NO_PROFILE = 'failed_no_profile'
	STATE_FAILED_PASSWORD_MISMTACH = 'password_mismatch'

	def login(self, salt: str, given_profile: Profile, success_cb: LoginSuccessCallback) -> Union[State, Session]:
		"""Logging in users

		Raises:
			autowp.core.shared.exceptions.VarTypeError: When given profile is not an instance of Profile
			autowp.core.shared.exceptions.ValidationError: When cannot validate given profile entity
		"""
		typechecker.check(given_profile, Profile, ('given_profile', 'Profile'))
		self.validate_profile(given_profile)

		profile = self.repo_profile.get_detail(given_profile.name)
		if not profile: # profile not exist
			return State(self.STATE_NAME, self.STATE_FAILED_NO_PROFILE, 'Profile not exist')

		if given_profile.password.to_hash() != profile.password.hashed:
			return State(self.STATE_NAME, self.STATE_FAILED_PASSWORD_MISMTACH, 'Password mismatch')

		# use callback to create a session object
		# we need to save this session to our data storage
		# and generate a new session object with an id from storage
		session_raw = success_cb(salt, profile)
		session_id = self.repo.register(session_raw)

		# generate new session
		session = Session(
			locked=False, 
			token=session_raw.token, 
			id=session_id, 
			profile_id=session_raw.profile_id
		)

		return session
