from dataclasses import dataclass

@dataclass(frozen=True)
class Profile:
	name: str 
	password: str
