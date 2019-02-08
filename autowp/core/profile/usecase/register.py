from typing import NoReturn, List

from autowp.core.shared.exceptions import StorageError 
from autowp.core.shared.utils import typechecker

from autowp.core.profile.entity import Profile
from autowp.core.profile.utils.validation import ValidateProfile
from autowp.core.profile.usecase.base import BaseProfileUseCase

class RegisterUseCase(BaseProfileUseCase, ValidateProfile):

	def register(self, profile: Profile) -> bool:
		"""Register new profile

		We need to check if given profile is an instance of Profile entiy
		We should validate given profile variable, need to validate

		Raises:
			core.shared.exceptions.VarTypeError: If profile is not an instance of Profile entity
			core.shared.exceptions.ValidationError: if profile not passed validation process
			core.shared.exceptions.StorageError: if there is an error related with datastorage 
		"""
		typechecker.check(profile, Profile, ('profile', 'Profile'))
		self.validate_profile(profile, self.repo)

		return self.repo.create(profile)
