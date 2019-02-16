import jwt
from typing import Optional, Dict, Any
from autowp.core.shared.base import Tokenizer

class JWTToken(Tokenizer):

	ALGO = 'HS256' 

	def encode(self) -> str:
		token = jwt.encode(self.payload, self.salt, algorithm=self.ALGO)
		return token

	def decode(self, token: str) -> Optional[Dict[str, Any]]:
		decoded = jwt.decode(token, self.salt, algorithms=self.ALGO)
		return decoded
