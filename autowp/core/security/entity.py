from typing import Dict, Any, Optional
from dataclasses import dataclass
from autowp.core.shared.base import Tokenizer

@dataclass(frozen=True)
class Token:
	"""This data class following standard JWT token

	Although this class designed to follow standard JWT token,
	token builder designed to be abstract, so should can to used
	any other tokenizer methods.
	"""
	salt: str
	payload: Dict[str, Any] 
	builder: Tokenizer
	options: Optional[Dict[str, Any]] = None

	def build(self) -> str:
		builder = self.builder(self.salt, self.payload, self.options)
		return builder.encode()

	def extract(self, data: Optional[str] = None) -> Optional[Dict[str, Any]]:
		builder = self.builder(salt, self.payload, self.options)
		return builder.decode(data)

@dataclass(frozen=True)
class Session:
	token: Token
	locked: bool
	id: Optional[str]  = None # should id from database
