from typing import NoReturn, Optional

from autowp.core.shared.exceptions import ValidationError, ValidationErrorMessage
from autowp.core.profile.entity import Profile
from autowp.core.profile.repository import ProfileRepository

class ValidateProfile(object):

	def validate_profile(self, profile: Profile, repo: Optional[ProfileRepository] = None) -> NoReturn:
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

		password = profile.password.raw
		if password == '':
			password_error_empty = ValidationErrorMessage('Password should not be empty')
			password_errors.append(password_error_empty)

		if profile.name == '' or not isinstance(profile.name, str):
			name_error_empty = ValidationErrorMessage('Profile name should not be empty value')
			name_errors.append(name_error_empty)

		if repo:
			# check if given name has been registered or not
			check = repo.get_detail(profile.name)
			if check:
				name_error_unique = ValidationErrorMessage(f'Given name: {profile.name} has been exist')
				name_errors.append(name_error_unique)

		if len(name_errors) >= 1:
			not_safe['name'] = name_errors

		if len(password_errors) >= 1:
			not_safe['password'] = password_errors

		if not_safe:
			raise ValidationError(not_safe)
