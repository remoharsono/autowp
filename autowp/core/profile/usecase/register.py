from typing import NoReturn, List

from autowp.core.profile.usecase.base import BaseProfileUseCase
from autowp.core.shared.exceptions import StorageError, ValidationError, ValidationErrorMessage, ValidationErrorMessages
from autowp.core.shared.utils import typechecker
from autowp.core.profile.entity import Profile

class RegisterUseCase(BaseProfileUseCase):

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
		self.validate(profile)

		return self.repo.create(profile)

	def validate(self, profile: Profile) -> NoReturn:
		"""Validate profile

		We need to valite given profile:
		- Name should not be empty
		- Name should be unique
		- Password should not be empty	

		Raises:
			core.shared.exceptions.ValidationError: When validation not passed	
		"""
		name_errors = []
		name_error_unique = ''
		name_error_empty = ''

		password_errors = []
		password_error_empty = ''

		not_safe = {}

		password = profile.password.to_hash()
		if password == '':
			password_error_empty = ValidationErrorMessage('Password should not be empty')
			password_errors.append(password_error_empty)

		if profile.name == '':
			name_error_empty = ValidationErrorMessage('Profile name should not be empty value')
			name_errors.append(name_error_empty)

		# check if given name has been registered or not
		check = self.repo.get_detail(profile.name)
		if check:
			name_error_unique = ValidationErrorMessage(f'Given name: {profile.name} has been exist')
			name_errors.append(name_error_unique)

		if len(name_errors) >= 1:
			not_safe['name'] = name_errors

		if len(password_errors) >= 1:
			not_safe['password'] = password_errors

		if not_safe:
			raise ValidationError(not_safe)
