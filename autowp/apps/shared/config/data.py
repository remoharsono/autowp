from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
	mongo_host: str
	mongo_dbname: str
	mongo_connect_timeout: int = 5000
	mongo_socket_timeout: int = 1000 
	mongo_server_selection_timeout: int = 15000
