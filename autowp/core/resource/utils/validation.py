from typing import NoReturn, Optional

from autowp.core.shared.exceptions import ValidationError, ValidationErrorMessage
from autowp.core.resource.entity import Server
from autowp.core.resource.repository import ResourceRepository  

class ValidateResource(object):

	def validate(self, server: Server, repo: Optional[ResourceRepository] = None) -> NoReturn:
		"""Validate resource 

		We need to valite given resource server entity:
		- Profile id should not be empty
		- Host should not be empty
		- Host should be unique
		- User should not be empty	

		Raises:
			core.shared.exceptions.ValidationError: When validation not passed	
		"""
		profile_errors = []
		profile_id_error_empty = ''

		host_errors = []
		host_error_empty = ''
		host_error_unique = ''

		user_errors = []
		user_error_empty = ''

		not_safe = {}

		if not isinstance(server.profile_id, str) or server.profile_id == '':
			profile_id_error_empty = ValidationErrorMessage('Profile id should not empty')
			profile_errors.append(profile_id_error_empty)

		if server.host == '' or not isinstance(server.host, str):
			host_error_empty = ValidationErrorMessage('Host should not be empty')
			host_errors.append(host_error_empty)

		if repo:
			check = repo.findByField('host', server.host) 
			if check:
				host_error_unique = ValidationErrorMessage('Host has been exist')
				host_errors.append(host_error_unique)

		if server.user == '' or not isinstance(server.user, str):
			user_error_empty = ValidationErrorMessage('User should not be empty')
			user_errors.append(user_error_empty)

		if len(profile_errors) >= 1:
			not_safe['profile'] = profile_errors

		if len(host_errors) >= 1:
			not_safe['host'] = host_errors

		if len(user_errors) >= 1:
			not_safe['user'] = user_errors

		if not_safe:
			raise ValidationError(not_safe) 
