from autowp.apps.shared.security.hasher import Sha256Hasher
from autowp.core.profile.entity import Profile, Password
from autowp.core.profile.repository import ProfileRepository 
from autowp.core.profile.usecase.register import RegisterUseCase

class RegisterAdapter(object):
	"""Act as proxy from application to core usecase"""

	def __init__(self, repo: ProfileRepository):
		self.usecase = RegisterUseCase(repo)

	def register(self, name: str, password: str) -> Profile:
		"""Register new profile based on given name and password
		
		Raises:
			core.shared.exceptions.ValidationError: if profile not passed validation process
			core.shared.exceptions.StorageError: if there is an error related with datastorage 
		"""
		password = Password(raw=password, hasher=Sha256Hasher)
		profile = Profile(name=name, password=password)
		return self.usecase.register(profile)
