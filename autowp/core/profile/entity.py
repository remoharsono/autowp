from dataclasses import dataclass
from autowp.core.shared.base import PasswordHasher

@dataclass(frozen=True)
class Password:
	raw: str
	hasher: PasswordHasher

	def to_hash(self) -> str:
		"""This method used to hash raw password"""
		hasher = self.hasher(self.raw)
		return hasher.hash()

@dataclass(frozen=True)
class Profile:
	name: str 
	password: Password 
