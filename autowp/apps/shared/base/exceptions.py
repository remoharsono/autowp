class AppError(Exception):
	def get_message(self) -> str:
		"""Get error message"""
		return self.message

class ConfigError(AppError):
	"""Used when need to trigger an error related with configurations"""

	def __init__(self, config_key: str, msg: str):
		self.message = f'Config key: {config_key} - {msg}'

class AuthError(AppError):
	"""Used when user try to running authenticated actions"""

	def __init__(self):
		self.message = 'Cannot continue your action, need to login first'
