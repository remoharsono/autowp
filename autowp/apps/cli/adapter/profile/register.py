from autowp.core.profile.entity import Profile
from autowp.core.profile.repository import ProfileRepository 
from autowp.core.profile.usecase.register import RegisterUseCase

class RegisterAdapter(object):

	def __init__(self, repo: ProfileRepository):
		self.usecase = RegisterUseCase(repo)
