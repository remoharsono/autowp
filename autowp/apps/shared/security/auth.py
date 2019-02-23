import functools

from autowp.apps.cli.repository.security import SecurityRepository
from autowp.apps.shared.config import config
from autowp.apps.shared.base.exceptions import AuthError

def auth(cls):

	@functools.wraps(cls)
	def wrapper_cls(*args, **kwargs):

		# check if session exist or not
		repo = SecurityRepository(config())
		if not repo.is_exist():
			raise AuthError()

		# create original adapter
		obj = cls(*args, **kwargs)
		return obj

	return wrapper_cls
