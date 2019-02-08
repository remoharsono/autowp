from typing import Optional, Dict, Any
from abc import ABCMeta, abstractmethod

class Repository(metaclass=ABCMeta):
	pass

class UseCase(metaclass=ABCMeta):
	pass

class PasswordHasher(metaclass=ABCMeta):
	"""This class should be used when hashing a raw 
	password using some hash algorithm

	Attributes:
		raw: A raw string
	"""

	def __init__(self, raw: str):
		self.raw = raw

	@abstractmethod
	def hash(self) -> str:
		"""This method should be implemented for any 
		hasher subclasses, to implement their hash algorithm
		"""
		pass

class Tokenizer(metaclass=ABCMeta):
	"""This class should be used when building session
	token

	Attributes:
		salt: A string act as salt		
		payload: A dictionary data that need to encode
		options: A dictionary used for options
	"""

	def __init__(self, salt: str, payload: dict, options: Optional[Dict[str, Any]] = None):
		self.salt = salt
		self.payload = payload
		self.options = options

	@abstractmethod
	def encode(self) -> str:
		pass

	@abstractmethod
	def decode(self, token: str) -> Optional[Dict[str, Any]]:
		pass
