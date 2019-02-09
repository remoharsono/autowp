import hashlib
from autowp.core.shared.base import PasswordHasher

class Sha256Hasher(PasswordHasher):

	ALGO_NAME = 'sha256'

	def hash(self) -> str:
		hasher = hashlib.new(self.ALGO_NAME)
		hasher.update(self.raw.encode())
		return hasher.hexdigest()
