class AppError(Exception):
	def get_message(self) -> str:
		"""Get error message"""
		return self.message

class ConfigError(AppError):
	"""Used when need to trigger an error related with configurations"""

	def __init__(self, config_key: str, msg: str):
		self.message = f'Config key: {config_key} - {msg}'
