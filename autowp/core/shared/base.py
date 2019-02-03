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
