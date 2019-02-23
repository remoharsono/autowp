from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Server:
	"""Server Entity

	What kind of data we need to handle
	about server as our resource:
	- profile_id
	- host (can be an ip or domain)
	- user 
	- custom key (optional) 
	- labels (a list of string and optional)
	- id (optional)
	"""
	profile_id: str
	host: str
	user: str
	sites: int = 0
	provider: Optional[str] = None
	custom_key: Optional[str] = None
	labels: Optional[List[str]] = None
	id: Optional[str] = None
