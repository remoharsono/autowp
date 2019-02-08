from dataclasses import dataclass

@dataclass(frozen=True)
class State:
	name: str
	status: str
	message: str
