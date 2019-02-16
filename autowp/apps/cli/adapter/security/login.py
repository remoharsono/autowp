from typing import Union, Callable, Optional

from autowp.core.shared.entity import State
from autowp.core.profile.entity import Profile, Password
from autowp.core.profile.repository import ProfileRepository
from autowp.core.security.repository import SecurityRepo 
from autowp.core.security.entity import Session, Token 
from autowp.core.security.usecase.login import LoginUseCase, LoginSuccessCallback
from autowp.apps.shared.security.hasher import Sha256Hasher
from autowp.apps.shared.security.tokenizer import JWTToken
from autowp.apps.shared.config import config, data

class LoginAdapter(object):

	def __init__(self, 
		repo_profile: ProfileRepository, 
		repo_sec: SecurityRepo, 
		config: data.Config):
		self.usecase = LoginUseCase(repo_profile, repo_sec)
		self.config = config

	def login(self, name: str, password: str) -> Union[State, Session]:
		"""Logging in users

		Raises:
			autowp.core.shared.exceptions.VarTypeError: When given profile is not an instance of Profile
			autowp.core.shared.exceptions.ValidationError: When cannot validate given profile entity
		"""
		password = Password(raw=password, hasher=Sha256Hasher)
		profile = Profile(name=name, password=password)
		session = self.usecase.login(self.config.salt, profile, self._login_success_callback)
		return session

	def _login_success_callback(self, salt: str, profile: Profile) -> Session:
		"""Build jwt token"""
		payload = {'name': profile.name}
		token = Token(salt=self.config.salt, payload=payload, builder=JWTToken)
		session = Session(token=token, locked=False)
		return session
